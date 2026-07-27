import pandas as pd
from typing import List, Any

def get_unique_values(df: pd.DataFrame, col_name: str) -> List[Any]:
    """Retrieve unique non-null values of a column, sorted for display."""
    if col_name not in df.columns:
        return []
    
    # Extract unique values, drop NaNs and convert to list
    uniques = df[col_name].dropna().unique()
    
    # Sort them nicely
    try:
        sorted_uniques = sorted(uniques)
    except TypeError:
        # Fallback if there are mixed types
        sorted_uniques = sorted(uniques, key=str)
        
    return [str(v) for v in sorted_uniques]

def filter_data(df: pd.DataFrame, col_name: str, value: str) -> pd.DataFrame:
    """Filter dataframe where the chosen column matches the specified value."""
    if not col_name or not value or col_name not in df.columns:
        return df

    # Cast column to string to allow exact/partial string matches
    # This also helps when matching numbers formatted as strings
    mask = df[col_name].astype(str) == str(value)
    return df[mask]

def sort_data(df: pd.DataFrame, col_name: str, direction: str) -> pd.DataFrame:
    """Sort dataframe based on column name and direction ('A-Z'/'Ascending' or 'Z-A'/'Descending')."""
    if not col_name or col_name not in df.columns:
        return df

    ascending = True
    if direction in ["Z-A", "Descending", "desc", "Z to A"]:
        ascending = False

    try:
        # Sort values. Put NaNs at the end
        return df.sort_values(by=col_name, ascending=ascending, na_position='last')
    except Exception:
        # Mixed types can fail to sort, convert to string temporarily for sorting if fail
        temp_col = df[col_name].astype(str)
        sorted_index = temp_col.sort_values(ascending=ascending).index
        return df.loc[sorted_index]
