
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

DATA = Path("../data/processed/au_banking_risk_scored.csv")
df = pd.read_csv(DATA)

features = [
    "age", "income", "credit_score", "loan_amount", "deposit_amount",
    "debt_to_income_ratio", "loan_to_deposit_ratio", "state",
    "occupation", "income_band", "bank_division", "product_type"
]
target = "default_flag"

X = df[features]
y = df[target]

numeric = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical = [c for c in X.columns if c not in numeric]

preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ("num", "passthrough", numeric),
])

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=180, max_depth=10, random_state=42)
}

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.25, random_state=42
)

for name, model in models.items():
    pipe = Pipeline([("prep", preprocess), ("model", model)])
    pipe.fit(X_train, y_train)
    proba = pipe.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    print(f"\n{name}")
    print("AUC:", round(roc_auc_score(y_test, proba), 3))
    print(classification_report(y_test, pred))

# Export final risk score for Power BI
best = Pipeline([("prep", preprocess), ("model", RandomForestClassifier(n_estimators=180, max_depth=10, random_state=42))])
best.fit(X_train, y_train)
df["ml_default_probability"] = best.predict_proba(X)[:, 1]
df["ml_risk_score"] = (df["ml_default_probability"] * 100).round(1)
df.to_csv("../data/processed/au_banking_risk_ml_scored.csv", index=False)
