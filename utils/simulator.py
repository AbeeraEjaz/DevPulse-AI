import os
import joblib
import pandas as pd
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

class PolicySimulatorEngine:
    def __init__(self):
        self.hdi_model = joblib.load(os.path.join(MODEL_DIR, 'hdi_model.pkl'))
        self.gdp_model = joblib.load(os.path.join(MODEL_DIR, 'gdp_model.pkl'))
        self.feature_names = joblib.load(os.path.join(MODEL_DIR, 'feature_columns.pkl'))

    def simulate_impact(self, baseline_dict, simulated_dict):
        """
        Baseline vs Policy Intervention values ka comparison karta hai
        aur exact projected growth compute karta hai.
        """
        # Create DataFrames
        df_base = pd.DataFrame([baseline_dict])[self.feature_names]
        df_sim = pd.DataFrame([simulated_dict])[self.feature_names]

        # Model Predictions
        base_hdi = float(self.hdi_model.predict(df_base)[0])
        sim_hdi = float(self.hdi_model.predict(df_sim)[0])

        base_gdp = float(self.gdp_model.predict(df_base)[0])
        sim_gdp = float(self.gdp_model.predict(df_sim)[0])

        # Calculate Deltas
        hdi_delta = sim_hdi - base_hdi
        hdi_pct_change = (hdi_delta / base_hdi) * 100 if base_hdi > 0 else 0

        gdp_delta = sim_gdp - base_gdp
        gdp_pct_change = (gdp_delta / base_gdp) * 100 if base_gdp > 0 else 0

        # Tier Evaluation
        def get_tier(score):
            if score < 0.550: return "Low Human Development"
            elif score < 0.700: return "Medium Human Development"
            elif score < 0.800: return "High Human Development"
            else: return "Very High Human Development"

        return {
            'baseline_hdi': round(base_hdi, 3),
            'simulated_hdi': round(sim_hdi, 3),
            'hdi_delta': round(hdi_delta, 3),
            'hdi_pct_change': round(hdi_pct_change, 2),
            'baseline_gdp': round(base_gdp, 2),
            'simulated_gdp': round(sim_gdp, 2),
            'gdp_delta': round(gdp_delta, 2),
            'gdp_pct_change': round(gdp_pct_change, 2),
            'baseline_tier': get_tier(base_hdi),
            'simulated_tier': get_tier(sim_hdi)
        }

if __name__ == "__main__":
    engine = PolicySimulatorEngine()
    
    # Test Baseline (e.g., Developing Country)
    base = {
        'Literacy_Rate_Adult_Pct': 59.0,
        'Life_Expectancy_Years': 66.5,
        'Access_to_Electricity_Pct': 75.0,
        'Renewable_Energy_Pct': 45.0,
        'Internet_Users_Pct': 25.0,
        'Infant_Mortality_Rate': 55.0
    }
    
    # Policy Intervention (+15% Literacy, +20% Internet)
    sim = base.copy()
    sim['Literacy_Rate_Adult_Pct'] = 74.0
    sim['Internet_Users_Pct'] = 45.0

    results = engine.simulate_impact(base, sim)
    print("Simulation Results:", results)