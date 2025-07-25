import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# Load the dataset
file_path = 'cleaned_dataset.csv'  # Replace with your dataset file path
data = pd.read_csv(file_path)

# Features - drop the target columns
X = data.drop(columns=['ID', 'Segmentation'])

# Encode any categorical features in X
for col in X.select_dtypes(include=['object', 'category']).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

# Hyperparameter grid and CV setup (same for both targets)
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0]
}v = StratifiedKFold(n_splits=2)

def train_and_evaluate(target_col):
    print(f"\n==== Training model for target: {target_col} ====")
    # Encode target variable
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(data[target_col])
    
    # Split data (stratify to keep label distribution balanced)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")
    
    # Initialize model
    model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')

    # Grid search
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring='accuracy',
        cv=cv,
        n_jobs=-1,
        verbose=1
    )
    grid_search.fit(X_train, y_train)
    
    print(f"Best parameters for {target_col} prediction: {grid_search.best_params_}")
    
    # Predict and report
    y_pred = grid_search.predict(X_test)
    print(f"Classification report for {target_col} prediction:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))


# Train and evaluate for both targets
train_and_evaluate('ID')
train_and_evaluate('Segmentation')
