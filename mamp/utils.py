"""
mamp utility module

"""
import os
import logging
import functools


log = logging.getLogger(__name__)


def ensure_single_run(fn=None, clear=False):
    """Ensures that function is not run twice 

    Apply the decorator on functions we only need to invoke once. 
    """
    memo = {}

    def decorator(func):
        if clear:
            memo.clear()

        @functools.wraps(func)
        def wrapper(*args):
            if args in memo:
                log.warning("call has already been performed on: {}".format(args))

                return memo[args]

            result = func(*args)
            memo[args] = result

            return result

        return wrapper

    if fn is not None:
        return decorator(fn)
    else:
        return decorator


def ensure_output_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

def increment_version_at(dirname):
    versions = [0]
    try:
        versions = [int(ver[1:]) for ver in os.listdir(dirname)]
    except OSError:
        pass

    return os.path.join(dirname, "v{:03d}".format(max(versions)+1))
