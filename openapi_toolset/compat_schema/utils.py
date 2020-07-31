def ensure_list(value):
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]
