
__all__ = ['auto_backend_wrapper']

import functools

def auto_backend_wrapper(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if hasattr(self, "save") and callable(getattr(self, "save")):
            self.save(result)
        if hasattr(self, "quit") and callable(getattr(self, "quit")):
            self.quit()
        return result
    return wrapper