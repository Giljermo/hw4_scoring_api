import functools
import logging

from redis import Redis
from redis.exceptions import TimeoutError, ConnectionError


class RunTimeConnectionError(Exception):
    pass


def redis_recall(max_retry_count):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while count < max_retry_count:
                try:
                    return func(*args, **kwargs)
                except (TimeoutError, ConnectionError) as err:
                    logging.error(f'Ошибка при подключении к хранилищу: {err}')
                    count += 1
                raise RunTimeConnectionError('Превышено число попыток подключения к хранилищу.')
        return wrapper
    return decorator


class Store:
    def __init__(self, host='localhost', port='6379', db=0, socket_timeout=5):
        self.host = host
        self.port = port
        self.db = db
        self.socket_timeout = socket_timeout

    @redis_recall(3)
    def get(self, key):
        redis_client = self.get_redis_client()
        value = redis_client.get(key)
        logging.info(f'Их хранилища redis по ключу "{key}" получено значение "{value}"')
        return value

    def cache_get(self, key):
        try:
            return self.get(key)
        except (RunTimeConnectionError, Exception) as err:
            logging.exception(err)

    @redis_recall(3)
    def cache_set(self, key, score, ttl):
        try:
            redis_client = self.get_redis_client()
            redis_client.set(key, score, ttl)
            logging.info(f'В хранилище redis записано значение "{score}" по ключу "{key}"')
        except RunTimeConnectionError as err:
            logging.error(err)

    def get_redis_client(self):
        return Redis(host=self.host,
                     port=self.port,
                     db=self.db,
                     socket_timeout=self.socket_timeout,
                     decode_responses=True)


if __name__ == '__main__':
    store = Store()
    score = 100
    store.cache_set('key1', score, 60*600)
    redis_val = store.get('key1')

    print(score, redis_val)