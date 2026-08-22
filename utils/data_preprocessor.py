import os
import pandas as pd
import numpy as np

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_development_data.csv')
PROCESSED_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed_hdi_data.csv')

def calculate_synthetic_hdi(df):
    """
    UNDP official methodology par based standard HDI index (0.0 to 1.0) compute karta hai:
    - Health Index: Life Expectancy (20 to 85 years scale)
    - Education Index: Adult Literacy + Internet Access proxy (0 to 100%)
    - Income Index: Log-scaled GDP Per Capita ($100 to $75,000 scale)
    HDI = Geometric Mean of (Health * Education * Income)
    """
    # 1. Health Index (Life Expectancy)
    le_min, le_max = 20.0, 85.0
    health_index = (df['Life_Expectancy_Years'] - le_min) / (le_max - le_min)
    health_index = health_index.clip(0.01, 1.0)

    # 2. Education & Tech Index
    edu_index = (0.7 * df['Literacy_Rate_Adult_Pct'] + 0.3 * df['Internet_Users_Pct']) / 100.0
    edu_index = edu_index.clip(0.01, 1.0)

    # 3. Income Index (Log Scale of GDP per Capita)
    gdp_min, gdp_max = 100.0, 75000.0
    gdp_clamped = df['GDP_Per_Capita_USD'].clip(gdp_min, gdp_max)
    income_index = (np.log(gdp_clamped) - np.log(gdp_min)) / (np.log(gdp_max) - np.log(gdp_min))
    income_index = income_index.clip(0.01, 1.0)

    # UNDP Composite Geometric Mean
    hdi = (health_index * edu_index * income_index) ** (1/3)
    return np.round(hdi, 4)


def clean_and_prepare_dataset():
    """
    Raw data ko clean karta hai, missing values impute karta hai aur HDI calculate karta hai.
    """
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError("Raw data file missing. Run data_loader.py first.")

    df = pd.read_csv(RAW_DATA_PATH)
    
    numeric_cols = [
        'Literacy_Rate_Adult_Pct',
        'Life_Expectancy_Years',
        'Access_to_Electricity_Pct',
        'Renewable_Energy_Pct',
        'Internet_Users_Pct',
        'Infant_Mortality_Rate',
        'GDP_Per_Capita_USD'
    ]

    # Convert numeric columns strictly
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Step A: Country-level forward/backward fill (agar kisi saal data miss ho)
    df[numeric_cols] = df.groupby('Country')[numeric_cols].transform(lambda x: x.ffill().bfill())

    # Step B: Global median imputation for still-missing values
    for col in numeric_cols:
        global_median = df[col].median()
        df[col] = df[col].fillna(global_median)

    # Step C: Compute Target Metric (HDI)
    df['Calculated_HDI'] = calculate_synthetic_hdi(df)

    # Step D: HDI Tier Categorization (UNDP Standards)
    df['HDI_Category'] = pd.cut(
        df['Calculated_HDI'],
        bins=[0.0, 0.550, 0.699, 0.799, 1.0],
        labels=['Low Human Development', 'Medium Human Development', 'High Human Development', 'Very High Human Development']
    )

    # Save to clean data storage
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"[SUCCESS] Cleaned dataset prepared with {len(df)} rows. Saved to: {PROCESSED_DATA_PATH}")
    return df


if __name__ == "__main__":
    df_clean = clean_and_prepare_dataset()
    print("Clean Data Sample:")
    print(df_clean[['Country', 'Year', 'Calculated_HDI', 'HDI_Category']].head(10))