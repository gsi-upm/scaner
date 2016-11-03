import argparse
import requests
import json
import glob
import multiprocessing
import datetime
from itertools import islice
from time import sleep, mktime
from os import path

parser = argparse.ArgumentParser(description="Populate the OrientDB database")
parser.add_argument('files', type=str,
                   help='folder or files to read tweets from')
parser.add_argument('--host', default='localhost:5000',
                   help='host where the service is running')
parser.add_argument('--limit', default=None, type=int,
                   help='limit for brand, timestamps and tweets, if specified')
parser.add_argument('--brand-limit', default=None, type=int,
                   help='limit of brand to load')
parser.add_argument('--timestamp-limit', default=None, type=int,
                    help='max number of timestamps files to read')
parser.add_argument('--tweet-limit', default=None, type=int,
                   help='max number of tweets to send')
parser.add_argument('--quiet', dest='verbose', action='store_false')
parser.set_defaults(verbose=True)
parser.add_argument('--parallel', dest='parallel', action='store_true',
                   help='use multiples processes to parallelize the loading')
parser.add_argument('--n-jobs', default=multiprocessing.cpu_count(), type=int,
                    help='number of processes used for parallelization requires parallel option active')
parser.set_defaults(parallel=False)

def set_limit(key, limit):
    x_limit = None
    if args[key] is None:
        x_limit = limit
    else:
        x_limit = args[key]
    return x_limit

def print_count(count, resp=None):
    if verbose and not resp is None and resp.status_code == 200:
        print("User added ({}). Resp. code: {}".format(str(count), resp.status_code))
    elif verbose and resp.status_code == 500:
        print("Error at {}".format(str(count)))
    elif verbose:
        print("User added ({})".format(str(count)))


def post_user(line, return_response=False, raw=False):
    user = line
    if not raw:
	    temp = user['raw']
    else:
        temp = user[1]

    user={}
    for k,v in temp.items():
        user[k] = v

    #time = user['created_at']
    topics = []
    topics.append(path.basename(brand.split('.')[0]))
    user['topics'] = topics
    #time = datetime.datetime.strptime(time, "%a %b %d %X %z %Y")
    #time = mktime(time.timetuple())
    #tweet['timestamp_ms'] = time
    
    print(user)
    r = requests.post(url, headers = headers, data=json.dumps(user))
    if return_response:
        return 1, r
    else:
        return 1

args = vars(parser.parse_args())

url = 'http://{host}/api/v1/users'.format(host=args['host'])
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

limit = args['limit']
verbose = args['verbose']
parallel = args['parallel']
n_jobs = args['n_jobs']

brand_limit = set_limit('brand_limit', limit)
timestamp_limit= set_limit('timestamp_limit', limit)
tweet_limit = set_limit('tweet_limit', limit)

if verbose:
    print('=Limits=')
    print('Brand: {},'.format(brand_limit),
          'Timestamp: {},'.format(timestamp_limit),
          'Tweet: {}'.format(tweet_limit))
    print('=')

counter = 0

in_path = path.abspath(args['files'])

if verbose:
    print('Reading from: {}'.format(in_path))

if __name__ == '__main__':

    if path.isdir(in_path):
        brand_list = [d for d in glob.glob(path.join(in_path, '*'))
                      if path.isdir(d)]
        if verbose:
            print('Brands to load from:',
                  (', '.join([path.basename(b) for b in islice(brand_list,
                                                              brand_limit)])))
        for brand in islice(brand_list, brand_limit):
            timestamps_list = glob.glob("{}/*".format(brand))
            for timestamp in islice(timestamps_list, timestamp_limit):
                with open(timestamp) as f:
                    a = json.load(f)
                    if not parallel:
                        for line in islice(a.items(), tweet_limit):
                            counter_, resp = post_user(line,
                                                         return_response=True, raw=True)
                            counter += counter_
                            if verbose:
                                print_count(counter, resp)

                    else:
                        with multiprocessing.Pool(n_jobs) as pool:
                            results = pool.map(post_user, f)
                        counter += sum(results)
                        print('Tweets added ({})'.format(counter))


    elif path.isfile(in_path):
        with open(in_path) as f:
            if not parallel:
                for line in islice(f, tweet_limit):
                    counter_, resp = post_user(line, return_response=True)
                    counter += counter_
                    if verbose:
                        print_count(counter, resp)
            else:
                with multiprocessing.Pool(n_jobs) as pool:
                    results = pool.map(post_user, f)
                counter += sum(results)
                print('Tweets added ({})'.format(counter))
