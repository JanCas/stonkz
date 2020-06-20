def pct_change(series):
    series_copy = series.copy()
    series_copy = series_copy.shift(1)
    return ((series - series_copy) / series_copy) * 100