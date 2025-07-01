from __future__ import annotations

import joblib
import pandas as pd
from pathlib import Path
from typing import Any, List

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import split_features_target, TARGET_COL


class LeadScorer:
    """Encapsulates the ML pipeline for training & predicting lead conversion probability."""

    def __init__(
        self,
        numeric_features: List[str] | None = None,
        categorical_features: List[str] | None = None,
    ) -> None:
        self.numeric_features = numeric_features
        self.categorical_features = categorical_features
        self.pipeline: Pipeline | None = None

    def _build_pipeline(self, X: pd.DataFrame) -> Pipeline:
        # Infer feature types if not provided
        numeric_features = (
            self.numeric_features if self.numeric_features is not None else X.select_dtypes(include=["number"]).columns.tolist()
        )
        categorical_features = (
            self.categorical_features if self.categorical_features is not None else X.select_dtypes(include=["object", "category"]).columns.tolist()
        )

        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown="ignore")

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features),
            ]
        )

        clf = LogisticRegression(max_iter=1000)

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", clf),
            ]
        )
        return pipeline

    def fit(self, df: pd.DataFrame, target_col: str = TARGET_COL) -> "LeadScorer":
        X, y = split_features_target(df, target_col)
        pipe = self._build_pipeline(X)
        pipe.fit(X, y)
        self.pipeline = pipe
        return self

    def predict_proba(self, df: pd.DataFrame) -> Any:
        if self.pipeline is None:
            raise ValueError("Model has not been trained or loaded.")
        return self.pipeline.predict_proba(df)[:, 1]  # probability of positive class

    def save(self, path: str | Path):
        if self.pipeline is None:
            raise ValueError("No model to save.")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, path)

    @classmethod
    def load(cls, path: str | Path) -> "LeadScorer":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        scorer = cls()
        scorer.pipeline = joblib.load(path)
        return scorer