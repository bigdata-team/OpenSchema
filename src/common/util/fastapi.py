def inject(func, *args, **kwargs):
    def _wrapped():
        return func(*args, **kwargs)

    return _wrapped


def unpack(func, *args, **kwargs):
    async def _unpack():
        async with func(*args, **kwargs) as o:
            yield o

    return _unpack
