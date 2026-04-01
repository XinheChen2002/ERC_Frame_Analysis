import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def read_csv():
  df = pd.read_excel("update 0223.xlsx")
  train_df = df[df["Category"].notna()]
  df_2022 = pd.read_excel("update 0223.xlsx", sheet_name="2022")
  df_2023 = pd.read_excel("update 0223.xlsx", sheet_name="2023")
  df_2024 = pd.read_excel("update 0223.xlsx", sheet_name="2024")
  return 

def 

train_df = train_df[train_df["Category"].notna()]

X_train_text = train_df["Design Method"]
y_train = train_df["Category"]

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2)
)

X_train = vectorizer.fit_transform(X_train_text)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    max_iter=500,
    class_weight="balanced"
)

model.fit(X_train, y_train)

train_pred = model.predict(X_train)

pd.crosstab(train_df["Category"], train_pred)

def predict_category(df):

    X_text = df["Design Method"]

    X_vec = vectorizer.transform(X_text)

    df["Category_pred"] = model.predict(X_vec)

    return df

df_2022 = predict_category(df_2022)
df_2023 = predict_category(df_2023)
df_2024 = predict_category(df_2024)

with pd.ExcelWriter("strategy_prediction.xlsx") as writer:

    train_df.to_excel(writer, sheet_name="2021", index=False)
    df_2022.to_excel(writer, sheet_name="2022", index=False)
    df_2023.to_excel(writer, sheet_name="2023", index=False)
    df_2024.to_excel(writer, sheet_name="2024", index=False)
