import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("final_dataset.csv")

X = df[["damage_score", "population", "hospitals", "roads"]]
y = df["priority"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=50, max_depth=6)
model.fit(X_train, y_train)

joblib.dump(model, "priority_model.pkl")
print("priority_model.pkl saved")
