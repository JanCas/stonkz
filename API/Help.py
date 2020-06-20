# TODO: Does not work yet!!!
def pct_change(series):
    series_copy = series.copy()
    series_copy = series_copy.shift(-1)
    return (series_copy - series) / series * 100