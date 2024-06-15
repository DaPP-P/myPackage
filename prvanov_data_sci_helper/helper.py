import pandas as pd;



# This function takes in a DataFrame and returns a DataFrame were the integer columns are converted to the smallest possible integer type.
# This can save a lot of memory when working with large datasets.
def shrink_ints(df):
    mapping = {}
    for col in df.dtypes[df.dtypes=='int64[pyarrow]'].index:
        max_ = df[col].max()
        min_ = df[col].min()
        if min_ < 0:
            continue
        if max_ < 255:
            mapping[col] = 'uint8[pyarrow]'
        elif max_ < 65_535:
            mapping[col] = 'uint16[pyarrow]'
        elif max_ <  4294967295:
            mapping[col] = 'uint32[pyarrow]'
    return df.astype(mapping)


# This function takes in a DataFrame, a column name and a an iqrRange and returns values that are iqrRange IQRs away from the median.
def calc_iqr_outlier(df, col, irqRange):
    ser = df[col]
    iqr = ser.quantile(.75) - ser.quantile(.25)
    med = ser.median()
    small_mask = ser < med-iqr*irqRange
    large_mask = ser > med+iqr*irqRange
    return small_mask | large_mask