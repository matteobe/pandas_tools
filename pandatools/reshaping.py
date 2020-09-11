# File: reshaping.pys
# Coding: utf-8
# Author: Matteo Berchier (matteo.berchier@gmail.com)
# Package: pandatools

# --------------- Summary --------------- #
# Extension tools for pandas

# --------------- Imports --------------- #
# External
import pandas as pd
import numpy as np
import multiprocessing as mp
from functools import partial


# Unique index creation
def unique_index(df: pd.DataFrame, index_name: str, columns: list,
                 sep: str = '_', date_format: str = '%Y-%m-%d %H:%M:%S', parallelize: bool = True) -> pd.DataFrame:

    if parallelize:
        n = mp.cpu_count()-1
        df_split = np.array_split(df, n)
        pool = mp.Pool(n)
        df = pd.concat(pool.map(partial(_unique_index, df=df_split, index_name=index_name,
                                        columns=columns, sep=sep, date_format=date_format)))
        pool.close()
        pool.join()
        return df
    else:
        return _unique_index(df, index_name, columns, sep=sep, date_format=date_format)


# Internal implementation of unique_index
def _unique_index(df: pd.DataFrame, index_name: str, columns: list,
                 sep: str = '_', date_format: str = '%Y-%m-%d %H:%M:%S') -> pd.DataFrame:

    # Check datatypes of different columns and transform to string if necessary
    for column in columns:
        col_type = df.dtypes[column].name
        if col_type == 'int64':
            df[column] = df[column].astype('str')
        elif col_type == 'float64':
            df[column] = df[column].astype('str')
        elif col_type == 'bool':
            df[column] = df[column].astype('str')
        elif col_type == 'datetime64':
            df[column] = df[column].dt.strftime(date_format)
        elif col_type == 'timedelta64':
            df[column] = df[column].astype('str')
        elif col_type == 'category':
            assert col_type == 'category', "Categorical data is not allowed for unique index building."

    # Merge indexes using inputted separator
    df.insert(loc=0, column=index_name, value=df[columns].agg(sep.join, axis=1))

    # Return new dataframe
    return df


# Separate merged index into custom columns
def separate_index(df: pd.DataFrame, index_name: str, columns: list,
                   sep: str = '_', drop_index: bool = False, parallelize: bool = True) -> pd.DataFrame:

    if parallelize:
        n = mp.cpu_count()-1
        df_split = np.array_split(df, n)
        pool = mp.Pool(n)
        df = pd.concat(pool.map(partial(_separate_index, df=df_split, index_name=index_name, columns=columns,
                                        sep=sep, drop_index=drop_index)))
        pool.close()
        pool.join()
        return df
    else:
        return _separate_index(df, index_name, columns, sep=sep, drop_index=drop_index)


# Internal implementation of separate_index
def _separate_index(df: pd.DataFrame, index_name: str, columns: list,
                    sep: str = '_', drop_index: bool = False) -> pd.DataFrame:

    # Check if multiple columns are passed in
    assert len(columns) > 1, "Only one column name has been passed in, minimum 2 column names required."

    # Split index_name column and create separate dataframe to pull from
    df_new = df[index_name].str.split(pat=sep, n=len(columns)-1, expand=True)

    # Build the new columns
    for idx, column in enumerate(columns):
        df.insert(loc=idx+1, column=column, value=df_new[idx])

    # Drop the unique index column
    if drop_index:
        df.drop(columns=index_name, inplace=True)

    return df
