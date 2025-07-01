# Repository for final project

This repository contains a reference implementation of a **Lead Scoring** system. It demonstrates how to:

1. Load tabular lead data from CSV files.
2. Train a machine-learning model (default: Logistic Regression) to predict the probability that a lead converts.
3. Persist the trained model to disk and use it later for scoring new leads.

## Project layout

```
.
├── lead_scoring/           ← Core Python package
│   ├── __init__.py
│   ├── data.py             ← Utilities for loading/validating data
│   ├── model.py            ← Model abstraction (train / save / load / predict)
│   └── pipeline.py         ← CLI entry-point to train + evaluate + save
├── notebooks/              ← (Optional) Jupyter notebooks for exploration
├── requirements.txt        ← Python dependencies
└── README.md
```

## Getting started

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Training

Prepare a CSV file where the target column is named `converted` and all other columns are numerical or categorical features. Then run:

```bash
python -m lead_scoring.pipeline \
  --train-path data/leads_train.csv \
  --model-path artifacts/lead_model.joblib
```

This will:

1. Load the CSV into a `pandas.DataFrame`.
2. Perform basic preprocessing (one-hot encode categoricals, impute missing values).
3. Train a logistic regression model.
4. Save the model to the specified location.

## Scoring new leads

After training, score new leads with:

```bash
python -m lead_scoring.pipeline \
  --predict-path data/leads_to_score.csv \
  --model-path artifacts/lead_model.joblib \
  --output-path scores.csv
```

The resulting `scores.csv` contains the original columns plus a new column `score` with the predicted conversion probability.

## Extending

- Swap out the estimator in `lead_scoring/model.py` (e.g., GradientBoosting, XGBoost).
- Add feature engineering steps in `lead_scoring/data.py`.
- Integrate with a REST API (FastAPI or Flask) for real-time scoring.

---

Feel free to adapt this scaffold to your own data and requirements.
