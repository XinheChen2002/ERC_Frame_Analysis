"""ERC typology classification pipeline.

Converted from the notebook `ERC_typology_ML.ipynb`.

What this script does:
1. Reads the ERC Excel workbook.
2. Uses rows with non-null `Category` values as labeled training data.
3. Vectorizes `Design Method` text with TF-IDF.
4. Trains a Logistic Regression classifier.
5. Predicts categories for the 2022, 2023, and 2024 sheets.
6. Writes the results to a new Excel workbook.
"""

from __future__ import annotations

from pathlib import Path
import argparse

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# -----------------------------
# Data loading
# -----------------------------
def load_workbook(input_path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the default sheet and the 2022-2024 sheets from the Excel workbook."""
    input_path = Path(input_path)

    df = pd.read_excel(input_path)
    df_2022 = pd.read_excel(input_path, sheet_name="2022")
    df_2023 = pd.read_excel(input_path, sheet_name="2023")
    df_2024 = pd.read_excel(input_path, sheet_name="2024")

    return df, df_2022, df_2023, df_2024


# -----------------------------
# Training preparation
# -----------------------------
def prepare_training_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Keep only labeled rows and extract training text and labels."""
    train_df = df[df["Category"].notna()].copy()

    # Fill missing text values to avoid vectorizer errors.
    train_df["Design Method"] = train_df["Design Method"].fillna("")

    x_train_text = train_df["Design Method"]
    y_train = train_df["Category"]

    return train_df, x_train_text, y_train


# -----------------------------
# Model training
# -----------------------------
def train_text_classifier(x_train_text: pd.Series, y_train: pd.Series) -> tuple[TfidfVectorizer, LogisticRegression]:
    """Vectorize text and train a Logistic Regression classifier."""
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )
    x_train = vectorizer.fit_transform(x_train_text)

    model = LogisticRegression(
        max_iter=500,
        class_weight="balanced",
    )
    model.fit(x_train, y_train)

    return vectorizer, model


# -----------------------------
# Prediction
# -----------------------------
def predict_category(df: pd.DataFrame, vectorizer: TfidfVectorizer, model: LogisticRegression) -> pd.DataFrame:
    """Predict categories for a dataframe using the trained model."""
    df = df.copy()
    df["Design Method"] = df["Design Method"].fillna("")

    x_text = df["Design Method"]
    x_vec = vectorizer.transform(x_text)
    df["Category_pred"] = model.predict(x_vec)

    return df


# -----------------------------
# Evaluation helper
# -----------------------------
def make_training_crosstab(
    train_df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    model: LogisticRegression,
) -> pd.DataFrame:
    """Return the notebook-style crosstab of actual vs predicted training labels."""
    x_train = vectorizer.transform(train_df["Design Method"].fillna(""))
    train_pred = model.predict(x_train)
    return pd.crosstab(train_df["Category"], train_pred)


# -----------------------------
# Output
# -----------------------------
def save_predictions(
    output_path: str | Path,
    train_df: pd.DataFrame,
    df_2022: pd.DataFrame,
    df_2023: pd.DataFrame,
    df_2024: pd.DataFrame,
    training_crosstab: pd.DataFrame | None = None,
) -> None:
    """Write predictions to an Excel workbook."""
    output_path = Path(output_path)

    with pd.ExcelWriter(output_path) as writer:
        train_df.to_excel(writer, sheet_name="2021", index=False)
        df_2022.to_excel(writer, sheet_name="2022", index=False)
        df_2023.to_excel(writer, sheet_name="2023", index=False)
        df_2024.to_excel(writer, sheet_name="2024", index=False)
        if training_crosstab is not None:
            training_crosstab.to_excel(writer, sheet_name="train_crosstab")


# -----------------------------
# Main workflow
# -----------------------------
def main(input_path: str | Path, output_path: str | Path) -> None:
    df, df_2022, df_2023, df_2024 = load_workbook(input_path)

    train_df, x_train_text, y_train = prepare_training_data(df)
    vectorizer, model = train_text_classifier(x_train_text, y_train)

    training_crosstab = make_training_crosstab(train_df, vectorizer, model)
    print("Training label distribution:")
    print(train_df["Category"].value_counts())
    print("\nTraining crosstab:")
    print(training_crosstab)

    df_2022 = predict_category(df_2022, vectorizer, model)
    df_2023 = predict_category(df_2023, vectorizer, model)
    df_2024 = predict_category(df_2024, vectorizer, model)

    save_predictions(
        output_path=output_path,
        train_df=train_df,
        df_2022=df_2022,
        df_2023=df_2023,
        df_2024=df_2024,
        training_crosstab=training_crosstab,
    )
    print(f"\nSaved prediction workbook to: {Path(output_path).resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ERC typology classifier and predict categories.")
    parser.add_argument(
        "--input",
        default="update 0223.xlsx",
        help="Path to the input Excel workbook. Default: update 0223.xlsx",
    )
    parser.add_argument(
        "--output",
        default="strategy_prediction.xlsx",
        help="Path to the output Excel workbook. Default: strategy_prediction.xlsx",
    )
    args = parser.parse_args()

    main(args.input, args.output)
