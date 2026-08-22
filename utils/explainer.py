import os
import joblib
import pandas as pd
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

def get_policy_feature_importance():
    """
    Random Forest aur Gradient Boosting models se feature importances
    extract karke ranked policy priorities calculate karta hai.
    """
    hdi_model_path = os.path.join(MODEL_DIR, 'hdi_model.pkl')
    features_path = os.path.join(MODEL_DIR, 'feature_columns.pkl')

    if not os.path.exists(hdi_model_path) or not os.path.exists(features_path):
        raise FileNotFoundError("Trained models not found. Run model_trainer.py first.")

    hdi_model = joblib.load(hdi_model_path)
    gdp_model = joblib.load(os.path.join(MODEL_DIR, 'gdp_model.pkl'))
    feature_names = joblib.load(features_path)

    # Readable labels for frontend display
    readable_labels = {
        'Literacy_Rate_Adult_Pct': 'Adult Literacy Rate (%)',
        'Life_Expectancy_Years': 'Life Expectancy (Years)',
        'Access_to_Electricity_Pct': 'Electricity Access (%)',
        'Renewable_Energy_Pct': 'Renewable Energy Mix (%)',
        'Internet_Users_Pct': 'Digital / Internet Adoption (%)',
        'Infant_Mortality_Rate': 'Infant Health / Survival Rate'
    }

    # Extract Importances
    hdi_importances = hdi_model.feature_importances_ * 100
    gdp_importances = gdp_model.feature_importances_ * 100

    df_importance = pd.DataFrame({
        'Feature_Code': feature_names,
        'Indicator': [readable_labels.get(f, f) for f in feature_names],
        'HDI_Impact_Pct': np.round(hdi_importances, 2),
        'GDP_Impact_Pct': np.round(gdp_importances, 2)
    }).sort_values(by='HDI_Impact_Pct', ascending=False).reset_index(drop=True)

    # Calculate Top Priority Insight
    top_driver = df_importance.iloc[0]['Indicator']
    top_weight = df_importance.iloc[0]['HDI_Impact_Pct']
    
    insight_text = (
        f"Key Finding: **{top_driver}** accounts for **{top_weight}%** of the variation "
        f"in global Human Development Index outcomes, making it the highest-priority policy lever."
    )

    return df_importance, insight_text


if __name__ == "__main__":
    df_imp, insight = get_policy_feature_importance()
    print("Policy Priority Ranking:")
    print(df_imp)
    print("\n" + insight)