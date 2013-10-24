from functools import wraps
import inspect

def initializer(fun):
    names, varargs, keywords, defaults = inspect.getargspec(fun)
    @wraps(fun)
    def wrapper(self, *args):
        for name, arg in zip(names[1:], args):
            setattr(self, name, arg)
        fun(self, *args)
    return wrapper
