
class memoize:
    def __init__(self, function):
        self.function = function
        self.store = {}

    def __call__(self, *args):
        key = (args)

        if not key in self.store:
            self.store[key] = self.function(*args)

        return self.store[key]

