import redis
import pickle
from GLOBALS import REDIS_HOST, REDIS_PORT

try:
    conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
except Exception as e:
    print(e)


# Redis get and set helper service

def set_cache(search_query, page, data_to_cache):
    try:
        # Pickling data to store in redis as it stores in binary
        data_to_cache = pickle.dumps(data_to_cache)
        # using redis HSET for setting values in format KEY, COUNT, VALUE
        conn.hset(search_query, str(page), data_to_cache)
    except Exception as set_exception:
        print(set_exception)


def get_cache(search_query, page):
    data = None
    try:
        data = conn.hget(search_query, str(page))
        data = pickle.loads(data)
        return data
    except Exception as get_exception:
        print(get_exception)
        return data
