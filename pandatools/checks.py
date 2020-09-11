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
    else:
        print("No duplicates found.")

    # Return dataframe without duplicates
    return df[~duplicates]


# Check uniqueness relation between ids
def check_onetoone(df: pd.DataFrame, key_col: str, map_col: str, printout: bool = True) -> bool:
    # Get relevant dataframe
    df_rel = df[[key_col, map_col]]
    df_rel = df_rel.drop_duplicates(keep='first')

    # Group by key_column values
    grouped = df_rel.groupby(key_col).agg({map_col: 'count'})

    # Find one-to-many relationships
    one_to_many = (grouped[map_col] > 1)

    # Print out warning if one-to-many exist
    if np.count_nonzero(one_to_many) > 0:
        if printout:
            print("Check failed: %d %s with multiple %s." % (np.count_nonzero(one_to_many), key_col, map_col))
            problem_ids = grouped[one_to_many]
            problem_rel = df_rel[df_rel[key_col].isin(list(problem_ids.index))]
            print(problem_rel.to_string(index=False))

        return False
    else:
        if printout:
            print("Check passed: %s and %s have 1-to-1 relationship." % (key_col, map_col))
        return True
