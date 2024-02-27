def flatten(nested):
    result = []
    try:
        # Don't iterate over string-like objects:
        try: nested + ''
        except TypeError: pass
        else: raise TypeError
        for sublist in nested:
            result.extend(flatten(sublist))
    except TypeError:
        result.append(nested)
    return result
