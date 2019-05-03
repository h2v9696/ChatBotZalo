class SingletonMeta(type):
    def __init__(self, *args, **kwargs):
        self._instance = None
        super(SingletonMeta, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(SingletonMeta, self).__call__(*args, **kwargs)
        return self._instance
