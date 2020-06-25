def pct_change(series):
    series_copy = series.copy()
    series_copy = series_copy.shift(1)
    return ((series - series_copy) / series_copy) * 100


def is_increasing(data, timeperiod):
    return data[-timeperiod] < data[-1]


def import_sklearn_module(sklearn_module):
    from importlib import import_module

    decomposed_string = sklearn_module.split('.')

    import_string = decomposed_string[0:2]
    model_name = decomposed_string[-1]

    return getattr(import_module(import_string), model_name)