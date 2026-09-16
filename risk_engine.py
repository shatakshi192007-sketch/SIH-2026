# risk_engine.py

def calculate_village_status(rainfall_mm, slope_deg, population, road_access):
    """
    Takes basic environmental and social facts about a village
    and calculates its hazard, risk, and relocation priority.
    """
    
    # 1. HAZARD SCORE (0.0 to 1.0)
    # High rainfall and steep slopes increase physical hazard danger
    rainfall_factor = min(rainfall_mm / 400.0, 1.0) # Caps at 400mm
    slope_factor = min(slope_deg / 60.0, 1.0)       # Caps at 60 degrees
    hazard_score = (rainfall_factor * 0.5) + (slope_factor * 0.5)
    
    # 2. VULNERABILITY SCORE (0.0 to 1.0)
    # Large populations with bad roads are highly vulnerable
    population_factor = min(population / 3000.0, 1.0) # Caps at 3000 people
    road_factor = 1.0 if road_access == "poor" else 0.2
    vulnerability_score = (population_factor * 0.4) + (road_factor * 0.6)
    
    # 3. COMPOSITE RISK SCORE (0.0 to 1.0)
    # Risk happens when a high hazard meets high vulnerability
    risk_score = round(hazard_score * vulnerability_score, 2)
    
    # 4. RED ZONE CLASSIFICATION
    # If the risk is 0.60 or higher, it enters the dynamic Red Zone
    is_red_zone = risk_score >= 0.60
    
    # 5. RELOCATION PRIORITY TRIAGE
    # We prioritize villages with critical risk scores
    if risk_score >= 0.70:
        priority = "IMMEDIATE"
    elif risk_score >= 0.40:
        priority = "SHORT TERM"
    else:
        priority = "MONITOR"
        
    return {
        "risk_score": risk_score,
        "is_red_zone": is_red_zone,
        "priority": priority,
        "raw_hazard": round(hazard_score, 2),
        "raw_vulnerability": round(vulnerability_score, 2)
    }

# --- TEST THE ENGINE ---
# This part lets you test your code locally to see if it works!
if __name__ == "__main__":
    # Test Village A: High rainfall, steep slope, poor roads (Should be Immediate)
    village_a = calculate_village_status(rainfall_mm=350, slope_deg=45, population=2500, road_access="poor")
    print("Village A Result:", village_a)
    
    # Test Village B: Low rainfall, flat land, good roads (Should be Monitor)
    village_b = calculate_village_status(rainfall_mm=100, slope_deg=5, population=400, road_access="good")
    print("Village B Result:", village_b)
