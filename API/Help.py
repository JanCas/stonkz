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

def construct_max(s1, s2):
    import pandas as pd
    assert(len(s1) == len(s2))

    max_list = []
    for x in range(0,len(s1)):
        max_list.append(max(s1[x], s2[x]))

    series = pd.Series(max_list)
    return series