import pandas as pd
from utils.generate_presets import generate_companies_csv

COMPANIES_CSV = "data/companies.csv"

def load_companies():
    # Generate preset if CSV doesn't exist
    #try:
    #    df = pd.read_csv(COMPANIES_CSV)
    #    print(f"Loaded {len(df)} companies from CSV.")
    #except FileNotFoundError:
    generate_companies_csv()
    df = pd.read_csv(COMPANIES_CSV)
    print(f"Loaded {len(df)} companies from CSV.")
    # Fill missing columns to avoid AgGrid issues
    required_cols = [
        "Name", "Sector", "WorldImpactScore", "Environmental", "Social", "Governance",
        "TransparencyIndex", "Scope1", "Scope2", "Scope3",
        "SustainabilityInvestmentRatio", "DataConfidence", "Report", "Remove"
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""
    return df