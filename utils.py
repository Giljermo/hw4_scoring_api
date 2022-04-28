import functools


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                try:
                    f(*new_args)
                except AssertionError as err:
                    raise AssertionError(f'Error: {err}\n Func name: {f.__name__}\n Case: {c}')
        return wrapper
    return decorator
