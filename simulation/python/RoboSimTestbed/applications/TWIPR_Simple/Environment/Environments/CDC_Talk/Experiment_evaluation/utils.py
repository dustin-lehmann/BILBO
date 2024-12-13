def _get_nested(data, *args):
    if args and data:
        element = args[0]
        if element:
            value = data.get(element)
            return value if len(args) == 1 else _get_nested(value, *args[1:])

def getSignal(sample_dict: dict, *args):
    out = [_get_nested(sample, *args) for sample in sample_dict]
    return out