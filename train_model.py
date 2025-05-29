import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

#mlflow.set_tracking_uri("sqlite:///mlruns.db")
mlflow.set_experiment("Linear regression example 2")

def train_linear_regression(alpha=0.5, l1_ratio=0.5, fit_intercept=True):
    with mlflow.start_run():
        np.random.seed(42)
        X = np.random.rand(100, 1) * 10
        y = 2 * X + 1 + np.random.randn(100, 1) * 2
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_param("fit_intercept", fit_intercept)

        model = LinearRegression(fit_intercept=fit_intercept)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        print(f"MLFlow runID: {mlflow.active_run().info.run_id}")
        print(f"    RMSE: {rmse:.4f}")
        print(f"    R2 score: {r2:.4f}")

        mlflow.sklearn.log_model(model, "linear_regression_model")

if __name__ == "__main__":
    # Run with different parameters to see multiple runs in MLflow UI
    print("--- Running first model (default parameters) ---")
    train_linear_regression()

    print("\n--- Running second model (fit_intercept=False) ---")
    train_linear_regression(fit_intercept=False)

    print("\n--- Running third model (different alpha/l1_ratio) ---")
    train_linear_regression(alpha=0.8, l1_ratio=0.2)

    print("\nMLflow runs completed. To view the UI, run 'mlflow ui' in your terminal.")
