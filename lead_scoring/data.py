from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Tuple

TARGET_COL = "converted"


def load_csv(csv_path: str | Path) -> pd.DataFrame:
    """Load leads from a CSV file into a DataFrame.

    Parameters
    ----------
    csv_path: str | Path
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    if TARGET_COL not in df.columns:
        raise ValueError(
            f"Target column '{TARGET_COL}' not found in dataset."
        )
    return df


def split_features_target(df: pd.DataFrame, target_col: str = TARGET_COL) -> Tuple[pd.DataFrame, pd.Series]:
    """Split a DataFrame into features X and target y."""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y