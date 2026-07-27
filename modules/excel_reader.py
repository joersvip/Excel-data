import os
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Tuple, Optional

class ExcelReader:
    _cached_df: Optional[pd.DataFrame] = None
    _active_file: str = "data/data.xlsx"
    _last_updated: str = "-"
    
    @classmethod
    def get_active_file_path(cls) -> str:
        return cls._active_file

    @classmethod
    def set_active_file_path(cls, path: str) -> None:
        cls._active_file = path
        cls._cached_df = None  # Invalidate cache

    @classmethod
    def load_data(cls, force_reload: bool = False) -> pd.DataFrame:
        """Load and cache Excel data from the active path with validation."""
        if cls._cached_df is not None and not force_reload:
            return cls._cached_df

        if not os.path.exists(cls._active_file):
            raise FileNotFoundError(f"File Excel tidak ditemukan di: {cls._active_file}")

        # Basic extension check
        _, ext = os.path.splitext(cls._active_file.lower())
        if ext not in ['.xlsx', '.xls']:
            raise ValueError(f"Format file tidak valid: {ext}. Harus berupa .xlsx atau .xls")

        try:
            # Read Excel file using pandas + openpyxl
            df = pd.read_excel(cls._active_file, engine='openpyxl')
        except Exception as e:
            raise IOError(f"File Excel rusak atau tidak dapat dibaca. Error: {str(e)}")

        if df.empty:
            raise ValueError("File Excel kosong (tidak memiliki baris data).")

        # Set default 'No' if it doesn't exist
        if 'No' not in df.columns:
            df.insert(0, 'No', range(1, len(df) + 1))

        # Fill NaNs with empty string or logical values
        # We preserve types but replace NaN with clean representations for UI
        cls._cached_df = df
        
        # Update last updated timestamp
        stat = os.stat(cls._active_file)
        cls._last_updated = datetime.fromtimestamp(stat.st_mtime).strftime("%d-%m-%Y %H:%M:%S")
        
        return cls._cached_df

    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        """Retrieve metadata for the loaded Excel sheet."""
        df = cls.load_data()
        file_size_kb = os.path.getsize(cls._active_file) / 1024
        
        return {
            "file_name": os.path.basename(cls._active_file),
            "file_path": cls._active_file,
            "total_rows": len(df),
            "total_cols": len(df.columns),
            "columns": list(df.columns),
            "last_updated": cls._last_updated,
            "file_size": f"{file_size_kb:.2f} KB" if file_size_kb < 1024 else f"{file_size_kb/1024:.2f} MB"
        }
