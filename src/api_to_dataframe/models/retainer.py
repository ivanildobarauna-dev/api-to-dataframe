import time


def RetryStrategies(func):
    print("Chamada a função RetryStrategies, com os params:", func)
    def wrapper(*args, **kwargs):
        print("Chamada do wrapper com os argumentos: ", args, kwargs)
    return wrapper
