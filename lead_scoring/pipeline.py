from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from .data import load_csv
from .model import LeadScorer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lead Scoring Training & Prediction Pipeline")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--train-path", type=str, help="CSV file containing training data (must include 'converted' column).")
    group.add_argument("--predict-path", type=str, help="CSV file with leads to score (no target column required).")

    parser.add_argument("--model-path", type=str, required=True, help="Path to save or load the model artifact (joblib file).")
    parser.add_argument("--output-path", type=str, help="Path to write scored leads as CSV (required when --predict-path is provided).")

    return parser.parse_args()


def train(train_csv: str, model_path: str):
    df = load_csv(train_csv)
    scorer = LeadScorer().fit(df)
    scorer.save(model_path)
    print(f"Model trained and saved to {model_path}")


def predict(predict_csv: str, model_path: str, output_path: str):
    df = pd.read_csv(predict_csv)
    scorer = LeadScorer.load(model_path)
    scores = scorer.predict_proba(df)
    df_out = df.copy()
    df_out["score"] = scores
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(output_path, index=False)
    print(f"Scores written to {output_path}")


def main():
    args = parse_args()

    if args.train_path:
        train(args.train_path, args.model_path)
    else:
        if args.output_path is None:
            raise ValueError("--output-path is required when --predict-path is provided.")
        predict(args.predict_path, args.model_path, args.output_path)


if __name__ == "__main__":
    main()