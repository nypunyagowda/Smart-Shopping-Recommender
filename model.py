import os
import joblib
import warnings
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

try:
    from xgboost import XGBClassifier
    xgboost_available = True
except ImportError:
    xgboost_available = False

warnings.filterwarnings("ignore")

# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

INPUT_FILE = os.path.join(DATA_DIR, "featured_dataset.csv")

MODEL_OUTPUT = os.path.join(MODEL_DIR, "model.pkl")

# =========================================================
# LOAD DATASET
# =========================================================

print("\n=================================================")
print("LOADING DATASET")
print("=================================================\n")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.\n")

# =========================================================
# SELECT FEATURES AND TARGET
# =========================================================

target_column = "is_sustainable"

feature_columns = [
    'category',
    'material',
    'brand',
    'price_usd',
    'rating',
    'reviews_count',
    'sustainability_label',
    'is_eco_material',
    'is_toxic_material',
    'is_biodegradable',
    'is_recyclable',
    'is_reusable',
    'is_plastic_free',
    'is_organic',
    'is_recycled_material',
    'eco_score'
]

X = df[feature_columns]
y = df[target_column]

print("Features and target selected.\n")

# =========================================================
# DEFINE COLUMN TYPES
# =========================================================

categorical_features = [
    'category',
    'material',
    'brand',
    'sustainability_label'
]

numerical_features = [
    'price_usd',
    'rating',
    'reviews_count',
    'eco_score',
    'is_eco_material',
    'is_toxic_material',
    'is_biodegradable',
    'is_recyclable',
    'is_reusable',
    'is_plastic_free',
    'is_organic',
    'is_recycled_material'
]

# =========================================================
# PREPROCESSING PIPELINE
# =========================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            'num',
            StandardScaler(),
            numerical_features
        ),
        (
            'cat',
            OneHotEncoder(handle_unknown='ignore'),
            categorical_features
        )
    ]
)

# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train-test split completed.\n")

print(f"Training samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")

# =========================================================
# MODEL DEFINITIONS
# =========================================================

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42
    )
}

if xgboost_available:
    models["XGBoost"] = XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='logloss',
        random_state=42
    )

# =========================================================
# TRAINING AND EVALUATION
# =========================================================

best_model = None
best_model_name = None
best_accuracy = 0

results = []

print("\n=================================================")
print("MODEL TRAINING STARTED")
print("=================================================\n")

for model_name, model in models.items():

    print(f"\nTraining {model_name}...")

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(y_test, y_pred)

    recall = recall_score(y_test, y_pred)

    f1 = f1_score(y_test, y_pred)

    results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })

    print("\nClassification Report:\n")

    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:\n")

    print(confusion_matrix(y_test, y_pred))

    print(f"\nAccuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = pipeline
        best_model_name = model_name

# =========================================================
# RESULTS SUMMARY
# =========================================================

results_df = pd.DataFrame(results)

print("\n=================================================")
print("MODEL COMPARISON")
print("=================================================\n")

print(results_df)

# =========================================================
# SAVE BEST MODEL
# =========================================================

joblib.dump(best_model, MODEL_OUTPUT)

print("\n=================================================")
print("BEST MODEL SAVED")
print("=================================================\n")

print(f"Best Model : {best_model_name}")
print(f"Accuracy   : {best_accuracy:.4f}")

print(f"\nModel saved to:")
print(MODEL_OUTPUT)

# =========================================================
# FEATURE IMPORTANCE (RANDOM FOREST ONLY)
# =========================================================

if best_model_name == "Random Forest":

    classifier = best_model.named_steps['classifier']

    try:
        importances = classifier.feature_importances_

        print("\nRandom Forest Feature Importances:\n")

        feature_names = numerical_features

        for feature, importance in zip(feature_names, importances[:len(feature_names)]):
            print(f"{feature:<25} {importance:.4f}")

    except:
        pass

# =========================================================
# FINAL MESSAGE
# =========================================================

print("\n=================================================")
print("MODEL TRAINING COMPLETED SUCCESSFULLY")
print("=================================================\n")