import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed_hdi_data.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

# Features jo model input ke taur par use karega
FEATURE_COLS = [
    'Literacy_Rate_Adult_Pct',
    'Life_Expectancy_Years',
    'Access_to_Electricity_Pct',
    'Renewable_Energy_Pct',
    'Internet_Users_Pct',
    'Infant_Mortality_Rate'
]

def train_and_evaluate_models():
    """
    Random Forest aur Gradient Boosting models ko train karke evaluation metrics
    compute karta hai aur best model ko disk par save karta hai.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Processed dataset not found. Run Phase 3 first.")

    df = pd.read_csv(DATA_PATH)
    
    # Features (X) aur Targets (y_hdi, y_gdp)
    X = df[FEATURE_COLS]
    y_hdi = df['Calculated_HDI']
    y_gdp = df['GDP_Per_Capita_USD']

    # Train-Test Split (80% Training, 20% Testing)
    X_train, X_test, y_hdi_train, y_hdi_test, y_gdp_train, y_gdp_test = train_test_split(
        X, y_hdi, y_gdp, test_size=0.2, random_state=42
    )

    print("=" * 50)
    print("🚀 Training HDI Prediction Model (Random Forest)...")
    hdi_model = RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1)
    hdi_model.fit(X_train, y_hdi_train)

    hdi_preds = hdi_model.predict(X_test)
    hdi_r2 = r2_score(y_hdi_test, hdi_preds)
    hdi_mae = mean_absolute_error(y_hdi_test, hdi_preds)
    hdi_rmse = np.sqrt(mean_squared_error(y_hdi_test, hdi_preds))

    print(f"✅ HDI Model Performance:")
    print(f"   • R² Score (Accuracy): {hdi_r2 * 100:.2f}%")
    print(f"   • Mean Absolute Error: {hdi_mae:.4f}")
    print(f"   • RMSE: {hdi_rmse:.4f}")

    print("=" * 50)
    print("🚀 Training GDP per Capita Model (Gradient Boosting)...")
    gdp_model = GradientBoostingRegressor(n_estimators=150, learning_rate=0.08, max_depth=5, random_state=42)
    gdp_model.fit(X_train, y_gdp_train)

    gdp_preds = gdp_model.predict(X_test)
    gdp_r2 = r2_score(y_gdp_test, gdp_preds)
    gdp_mae = mean_absolute_error(y_gdp_test, gdp_preds)

    print(f"✅ GDP Model Performance:")
    print(f"   • R² Score (Accuracy): {gdp_r2 * 100:.2f}%")
    print(f"   • Mean Absolute Error: ${gdp_mae:,.2f}")
    print("=" * 50)

    # Models aur metadata ko models/ folder me save karna
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    joblib.dump(hdi_model, os.path.join(MODEL_DIR, 'hdi_model.pkl'))
    joblib.dump(gdp_model, os.path.join(MODEL_DIR, 'gdp_model.pkl'))
    
    # Feature names save karna inference ke liye
    joblib.dump(FEATURE_COLS, os.path.join(MODEL_DIR, 'feature_columns.pkl'))

    # Metrics dictionary return karna taake UI par show kar sakein
    metrics = {
        'hdi_r2': round(hdi_r2 * 100, 2),
        'hdi_mae': round(hdi_mae, 4),
        'gdp_r2': round(gdp_r2 * 100, 2),
        'gdp_mae': round(gdp_mae, 2)
    }
    joblib.dump(metrics, os.path.join(MODEL_DIR, 'model_metrics.pkl'))
    
    print("[SUCCESS] Models & Metrics successfully saved to 'models/' directory.")
    return metrics


if __name__ == "__main__":
    train_and_evaluate_models()