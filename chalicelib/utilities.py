import logging
from chalice import Chalice
from functools import wraps
from time import time

app = Chalice(app_name='datapipeline-chalice')
logger = app.log
logger.setLevel(logging.DEBUG)


def logs_decorator(func):
        @wraps(func)
        def decor(*args, **kwargs):
            logger.info(
                f'Running: {func.__module__} -> {func.__name__}')
            ts = time()
            result = func(*args, **kwargs)
            te = time()
            logger.info(
                f'Completed:{func.__module__} -> {func.__name__}; ' +
                f'took: {te-ts:.3f} sec')
            return result

        return decor
