import pandas as pd

def search_data(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Search for a string query in any column of the dataframe."""
    if not query or not query.strip():
        return df

    query = str(query).strip().lower()
    
    # Cast elements as strings and look for substring matches across any column
    # Use lowercase comparison to ensure case-insensitive matching
    mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(query, regex=False)).any(axis=1)
    
    return df[mask]
