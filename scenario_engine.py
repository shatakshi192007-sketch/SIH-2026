# scenario_engine.py
from ml_risk_engine import cluster_village_risks

def run_climate_scenario(base_villages: list, rainfall_multiplier: float, structural_damage_multiplier: float):
    """
    Simulates environmental disasters by applying multipliers to the baseline dataset 
    and recalculating the Machine Learning clusters on the fly.
    """
    simulated_dataset = []
    
    for v in base_villages:
        simulated_village = v.copy()
        
        # Apply the scenario modifiers (e.g., rainfall increases by 30% -> multiplier = 1.30)
        simulated_village['rainfall_mm'] = v['rainfall_mm'] * rainfall_multiplier
        
        # If roads degrade due to heavy rain, force the status to "poor"
        if structural_damage_multiplier > 1.20 and v['road_access'] == "moderate":
            simulated_village['road_access'] = "poor"
            
        simulated_dataset.append(simulated_village)
        
    # Re-run the data through your ML clustering algorithm under the new stress conditions
    scenario_output = cluster_village_risks(simulated_dataset)
    return scenario_output

# --- TEST THE SCENARIO ENGINE ---
if __name__ == "__main__":
    # Baseline dataset
    historical_villages = [
        {"name": "Village Alpha", "lat": 25.612, "lon": 85.137, "rainfall_mm": 250, "slope_deg": 40, "population": 2800, "road_access": "moderate"},
        {"name": "Village Beta", "lat": 25.620, "lon": 85.145, "rainfall_mm": 100, "slope_deg": 8,  "population": 350,  "road_access": "good"}
    ]
    
    print("--- BASELINE CONDITIONS ---")
    base = cluster_village_risks(historical_villages)
    for v in base:
        print(f"{v['name']} Priority: {v['ml_cluster_priority']}")
        
    print("\n--- SIMULATING +40% EXTREME RAINFALL CLOUDBURST ---")
    # 1.40 means a 40% increase in rainfall intensity
    disaster_scenario = run_climate_scenario(historical_villages, rainfall_multiplier=1.40, structural_damage_multiplier=1.30)
    for v in disaster_scenario:
        print(f"{v['name']} New Priority: {v['ml_cluster_priority']} (New Risk Score: {v['risk_score']})")
