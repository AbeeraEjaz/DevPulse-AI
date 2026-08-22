import os
import pandas as pd
import wbgapi as wb

# UNDP aur World Bank Core Development Indicators
INDICATORS = {
    'SE.ADT.LITR.ZS': 'Literacy_Rate_Adult_Pct',
    'SP.DYN.LE00.IN': 'Life_Expectancy_Years',
    'EG.ELC.ACCS.ZS': 'Access_to_Electricity_Pct',
    'EG.FEC.RNEW.ZS': 'Renewable_Energy_Pct',
    'IT.NET.USER.ZS': 'Internet_Users_Pct',
    'SH.DYN.MORT': 'Infant_Mortality_Rate',
    'NY.GDP.PCAP.CD': 'GDP_Per_Capita_USD'
}

DATA_CACHE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_development_data.csv')


def fetch_world_bank_data(start_year=2005, end_year=2023):
    """
    World Bank API se verified data fetch karke clean long/wide format me store karta hai.
    """
    if os.path.exists(DATA_CACHE_PATH):
        df = pd.read_csv(DATA_CACHE_PATH)
        if not df.empty:
            print("[INFO] Loading cached World Bank data...")
            return df

    print(f"[INFO] Fetching World Bank dataset ({start_year}-{end_year})...")
    
    records = []
    years = list(range(start_year, end_year + 1))
    
    # Direct reliable batch query
    for code, col_name in INDICATORS.items():
        try:
            print(f"Fetching: {col_name}...")
            raw = wb.data.DataFrame(code, time=years, labels=True, numericTimeKeys=True)
            raw = raw.reset_index()
            
            # Melt year columns
            year_cols = [y for y in years if y in raw.columns]
            melted = pd.melt(
                raw,
                id_vars=['economy', 'Country'],
                value_vars=year_cols,
                var_name='Year',
                value_name=col_name
            )
            records.append(melted)
        except Exception as e:
            print(f"Error fetching {code}: {e}")

    if not records:
        print("[ERROR] No data fetched from World Bank API.")
        return pd.DataFrame()

    # Sare indicators ko merge karna
    final_df = records[0]
    for r in records[1:]:
        final_df = pd.merge(final_df, r, on=['economy', 'Country', 'Year'], how='outer')

    final_df.rename(columns={'economy': 'Country_Code'}, inplace=True)
    final_df['Year'] = final_df['Year'].astype(int)

    # Save cache
    os.makedirs(os.path.dirname(DATA_CACHE_PATH), exist_ok=True)
    final_df.to_csv(DATA_CACHE_PATH, index=False)
    print(f"[SUCCESS] Saved {len(final_df)} rows to {DATA_CACHE_PATH}")
    return final_df


if __name__ == "__main__":
    df = fetch_world_bank_data(start_year=2005, end_year=2023)
    print(f"Total Rows: {len(df)}, Total Countries: {df['Country'].nunique()}")