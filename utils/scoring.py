import math
from typing import Dict, Any
import numpy as np

def compute_world_impact_score(row: dict) -> dict:
    """
    Weighted World Impact Score: 
    60% Environmental, 25% Social, 15% Governance
    Adjusted for SustainabilityInvestmentRatio and DataConfidence.
    """
    env = float(row.get("Environmental") or 50)
    soc = float(row.get("Social") or 50)
    gov = float(row.get("Governance") or 50)
    invest = float(row.get("SustainabilityInvestmentRatio") or 0)
    conf = float(row.get("DataConfidence") or 50)

    raw = 0.6*env + 0.25*soc + 0.15*gov
    conf_multiplier = 0.7 + 0.3*(conf/100)
    invest_bonus = min(invest, 0.10)

    final_score = min(100, raw*conf_multiplier*(1+invest_bonus))

    return {"final_score": round(final_score,2)}

