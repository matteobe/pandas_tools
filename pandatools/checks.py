# File: checks.py
# Coding: utf-8
# Author: Matteo Berchier (matteo.berchier@gmail.com)
# Package: pandatools

# --------------- Summary --------------- #
# Checks for data integrity

# --------------- Imports --------------- #
# External
import pandas as pd
import numpy as np


# Check and remove duplicates
def clean_duplicates(df: pd.DataFrame, columns: list, keep: str = 'first') -> pd.DataFrame:
    # Get duplicates count
    duplicates = df.duplicated(subset=columns, keep=keep)
    duplicates_count = np.count_nonzero(duplicates)

    # Tell user if duplicates are present
    if duplicates_count > 0:
        print("Duplicates present: %d" % duplicates_count)

    # Return dataframe without duplicates
    return df[~duplicates]


# Check uniqueness relation between ids
def check_onetoone(df: pd.DataFrame, key_col: str, map_col: str) -> bool:
    # Group dataframe columns
    grouped = df.groupby(key_col).agg({map_col: 'count'})

    # Find one-to-many relationships
    one_to_many = (grouped[map_col] > 1)

    # Print out warning if one-to-many exist
    if np.count_nonzero(one_to_many) > 0:
        print("Check failed: %d %s with multiple %s." % (np.count_nonzero(one_to_many), key_col, map_col))
        return False
    else:
        print("Check passed: %s and %s have 1-to-1 relationship." % (key_col, map_col))
        return True
