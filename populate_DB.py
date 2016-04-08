import requests
import json
import glob
from itertools import islice
from time import sleep

limit = None

url = 'http://localhost:5000/api/v1/tweets'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
counter = 0

list_of_brands =  glob.glob("./tweet_data/*")
for brand in islice(list_of_brands, limit):
    list_of_dates = glob.glob("{brand}/*".format(brand=brand))
    for date in islice(list_of_dates, limit):
        with open(date) as f:
            for line in islice(f, limit):
                
                #sleep(1)
                tweet_full = json.loads(line)
                temp = tweet_full['raw']
                tweet={}
                for k,v in temp.items():
                    if v:
                        tweet[k] = v
                # print(json.dumps(tweet))
                r = requests.post(url, headers = headers, data=json.dumps(tweet))
                print(r)
                # print("Tweet added")
                counter += 1
                print("Tweets in DB = " + str(counter))
