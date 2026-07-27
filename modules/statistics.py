import pandas as pd
from typing import Dict, List, Any, Tuple

def analyze_columns(df: pd.DataFrame) -> Dict[str, Any]:
    """Scan the dataframe and identify potential categorical and numeric columns."""
    categorical_cols = []
    numeric_cols = []
    
    for col in df.columns:
        if col == "No":
            continue
            
        # Check if numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            # If it has very few unique values, could be categorized, but we'll treat it as numeric if it is float/int
            numeric_cols.append(col)
        else:
            # Check unique count to determine if it is a good categorical candidate
            try:
                unique_count = df[col].nunique()
                if 1 < unique_count <= 25:  # Ideal for bar/pie charts
                    categorical_cols.append(col)
            except Exception:
                pass
                
    # If no categorical columns found, fall back to any string columns with <= 50 unique values
    if not categorical_cols:
        for col in df.columns:
            if col == "No":
                continue
            try:
                unique_count = df[col].nunique()
                if unique_count <= 50:
                    categorical_cols.append(col)
            except Exception:
                pass

    return {
        "categorical": categorical_cols,
        "numeric": numeric_cols
    }

def get_categorical_stats(df: pd.DataFrame, col_name: str) -> List[Tuple[str, int, float]]:
    """Get the distribution (count and percentage) of values in a categorical column."""
    if col_name not in df.columns:
        return []
        
    counts = df[col_name].fillna("Kosong").astype(str).value_counts()
    total = len(df)
    
    result = []
    for val, count in counts.items():
        percentage = (count / total) * 100
        result.append((str(val), int(count), float(percentage)))
        
    return result

def get_numeric_stats(df: pd.DataFrame, col_name: str) -> Dict[str, Any]:
    """Get descriptive statistics for a numeric column."""
    if col_name not in df.columns:
        return {}
        
    series = df[col_name].dropna()
    if series.empty:
        return {
            "count": 0, "sum": 0, "mean": 0, "min": 0, "max": 0, "median": 0
        }
        
    return {
        "count": int(series.count()),
        "sum": float(series.sum()),
        "mean": float(series.mean()),
        "min": float(series.min()),
        "max": float(series.max()),
        "median": float(series.median())
    }
