import time
from enum import Enum


class Strategies(Enum):
    NoRetryStrategy = 0
    LinearRetryStrategy = 1
    ExponentialRetryStrategy = 2


def RetryStrategies(func):
    def wrapper(*args, **kwargs):
        attemp = 0
        while attemp < args[0].retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attemp += 1

                if args[0].retry_strategy == Strategies.NoRetryStrategy:
                    break
                elif args[0].retry_strategy == Strategies.LinearRetryStrategy:
                    time.sleep(args[0].delay)
                elif args[0].retry_strategy == Strategies.ExponentialRetryStrategy:
                    time.sleep(args[0].delay * 2 ** attemp)

                if attemp == args[0].retries:
                    print(f"Failed after {args[0].retries} attempts")
                    raise e
    return wrapper