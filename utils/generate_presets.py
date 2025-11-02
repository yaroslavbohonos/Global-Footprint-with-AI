import os
import time
import pandas as pd
from utils.api_clients import extract_company_esg
from utils.scoring import compute_world_impact_score

OUTPUT_FILE = "data/companies.csv"
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

PRESET_COMPANIES = [
    "ExxonMobil", "Chevron", "Shell", "BP", "TotalEnergies",
    "Saudi Aramco", "Volkswagen", "Toyota"
]

CSV_COLUMNS = [
    "Name",
    "Sector",
    "World Impact Score",
    "Environmental",
    "Social",
    "Governance",
    "Transparency Index",
    "Scope 1-3 Emissions",
    "Sustainability Investment Ratio",
    "Data Confidence",
    "Report",
    "Remove"
]

def generate_companies_csv(companies=PRESET_COMPANIES, out_file=OUTPUT_FILE):
    all_rows = []

    for name in companies:
        try:
            esg_data = extract_company_esg(name)
            
            # sum Scope 1-3 emissions
            scope_total = sum([
                esg_data.get("Scope1", 0),
                esg_data.get("Scope2", 0),
                esg_data.get("Scope3", 0)
            ])

            # compute world impact score
            world_impact = compute_world_impact_score(esg_data)["final_score"]

            row = {
                "Name": name,
                "Sector": esg_data.get("Sector", "Unknown"),
                "World Impact Score": world_impact,
                "Environmental": esg_data.get("Environmental", 0),
                "Social": esg_data.get("Social", 0),
                "Governance": esg_data.get("Governance", 0),
                "Transparency Index": esg_data.get("TransparencyIndex", 0),
                "Scope 1-3 Emissions": scope_total,
                "Sustainability Investment Ratio": esg_data.get("SustainabilityInvestmentRatio", 0),
                "Data Confidence": esg_data.get("DataConfidence", 0),
                "Report": "",
                "Remove": ""
            }
            all_rows.append(row)

        except Exception as e:
            print(f"Failed to get data for {name}: {e}")
            # fallback row
            fallback = {col: 0 if col not in ["Name", "Sector", "Report", "Remove"] else "" for col in CSV_COLUMNS}
            fallback["Name"] = name
            fallback["Sector"] = "Unknown"
            all_rows.append(fallback)

    df = pd.DataFrame(all_rows, columns=CSV_COLUMNS)
    df.to_csv(out_file, index=False, encoding="utf-8")
    print(f"Saved {len(df)} rows to {out_file}")

if __name__ == "__main__":
    generate_companies_csv()