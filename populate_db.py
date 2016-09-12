import argparse
import requests
import json
import glob
from itertools import islice
from time import sleep
from os import path

parser = argparse.ArgumentParser(description="Populate the OrientDB database")
parser.add_argument('files', type=str,
                   help='folder or files to read tweets from')
parser.add_argument('--host', default='localhost:5000',
                   help='host where the service is running')
parser.add_argument('--limit', default=None, type=int,
                   help='limit for both brand and tweets, if specified')
parser.add_argument('--brand-limit', default=None, type=int,
                   help='limit of brand to load')
parser.add_argument('--timestamp-limit', default=None, type=int,
                    help='max number of timestamps files to read')
parser.add_argument('--tweet-limit', default=None, type=int,
                   help='max number of tweets to send')
parser.add_argument('--quiet', dest='verbose', action='store_false')
parser.set_defaults(verbose=True)


def set_limit(key, limit):
    x_limit = None
    if args[key] is None:
        x_limit = limit
    else:
        x_limit = args[key]
    return x_limit

def post_tweet(line, url, headers, counter):
    tweet_full = json.loads(line)
    temp = tweet_full['raw']
    tweet={}
    for k,v in temp.items():
        if v:
            tweet[k] = v

    r = requests.post(url, headers = headers, data=json.dumps(tweet))
    counter += 1
    if verbose:
        print("Tweet added ({})".format(str(counter)))
    return counter

args = vars(parser.parse_args())

url = 'http://{host}/api/v1/tweets'.format(host=args['host'])
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

limit = args['limit']
verbose = args['verbose']

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
        brand_list = glob.glob(path.join(in_path, '*'))
        if verbose:
            print('Brands to load from:',
                  (' '.join([path.basename(b) for b in islice(brand_list,
                                                     brand_limit)])))
        for brand in islice(brand_list, brand_limit):
            timestamps_list = glob.glob("{}/*".format(brand))
            for timestamp in islice(timestamps_list, timestamp_limit):
                with open(timestamp) as f:
                    for line in islice(f, tweet_limit):
                        counter = post_tweet(line, url, headers, counter)
    elif path.isfile(in_path):
        with open(in_path) as f:
            for line in islice(f, tweet_limit):
                counter = post_tweet(line, url, headers, counter)
