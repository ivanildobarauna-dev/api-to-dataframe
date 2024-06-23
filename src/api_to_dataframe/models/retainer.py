import time
from enum import Enum


class Strategies(Enum):
    NoRetryStrategy = 0
    LinearRetryStrategy = 1
    ExponentialRetryStrategy = 2


def RetryStrategies(func):
    def wrapper(*args, **kwargs):
        retry_number = 0
        while retry_number < args[0].retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                retry_number += 1

                if args[0].retry_strategy == Strategies.NoRetryStrategy:
                    raise e
                elif args[0].retry_strategy == Strategies.LinearRetryStrategy:
                    time.sleep(args[0].delay)
                elif args[0].retry_strategy == Strategies.ExponentialRetryStrategy:
                    time.sleep(args[0].delay * 2 ** retry_number)

                if retry_number == args[0].retries:
                    print(f"Failed after {retry_number} retries using {args[0].retry_strategy}")
                    raise e
    return wrapper
