from os import path
import pickle


def load_cache():
    global __CACHE
    if path.exists('cache.pickle'):
        with open('cache.pickle', 'rb') as f:
            __CACHE = pickle.load(f)
    else:
        __CACHE = dict()


def save_cache():
    with open('cache.pickle', 'wb') as f:
        pickle.dump(__CACHE, f)


def get(key: str) -> any:
    return __CACHE.get(key)


def set(key: str, value: any):
    __CACHE[key] = value


def has(key: str) -> bool:
    return key in __CACHE
