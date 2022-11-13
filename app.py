import argparse
import random
import string
import redis
import time

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--id")
parser.add_argument("-key", "--key")
parser.add_argument("-ttl", "--ttl")
parser.add_argument("-sleep", "--sleep")
args = parser.parse_args()

id = int(args.id) if args.id else None
if id is None:
    raise Exception("Please set argument --id.")

key = args.key if args.key else 'testKey'
ttl = int(args.ttl) if args.ttl else 30
sleep = float(args.sleep) if args.sleep else 1.0

ttlRefreshCache = 0.1 * ttl
ttlRefreshDecision = ttlRefreshCache / 2

r = redis.Redis(host='localhost', port=6379)

while True:
    ttl_last = r.ttl(name=key)
    print(f"ID: {id}. TTL last: {ttl_last} seconds")
    if ttl_last > ttlRefreshCache:
        print(f"ID: {id}. Used cache.")
        print(f"ID: {id}. Value: '{r.get(name=key)}'")
    elif ttl_last < 0:
        print(f"ID: {id}. Key '{key}' missed in cache.")
        print(f"ID: {id}. Get value from source.")
        value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print(f"ID: {id}. Value: '{value}'")
        r.set(name=key, value=value, ex=ttl)
    else:
        p = (random.randrange((ttlRefreshCache - ttl_last)*100, ttlRefreshCache*100, 1) / 100)   
        print(f"ID: {id}. Probability: {p}. Decision: value > {ttlRefreshDecision}.")     
        if p >= ttlRefreshDecision:        
            print(f"ID: {id}. Used probabilistic cache.")
            print(f"ID: {id}. Get value from source.")
            value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            print(f"ID: {id}. Value: '{value}'")
            r.set(name=key, value=value, ex=ttl)
        else:
            print(f"ID: {id}. Used cache.")
            print(f"ID: {id}. Value: '{r.get(name=key)}'")
    print('#################################################')
    time.sleep(sleep)