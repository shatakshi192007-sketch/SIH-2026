import json
import numpy as np
from sklearn.cluster import KMeans
from risk_engine import calculate_village_status

def cluster_village_risks(villages_list: list):
    features = []
    processed_villages = []
    
    for v in villages_list:
        status = calculate_village_status(
            v['rainfall_mm'], v['slope_deg'], v['population'], v['road_access']
        )
        features.append([status['raw_hazard'], status['raw_vulnerability']])
        
        v_meta = v.copy()
        v_meta.update(status)
        processed_villages.append(v_meta)
        
    X = np.array(features)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    cluster_labels = kmeans.fit_predict(X)
    
    centers = kmeans.cluster_centers_
    sorted_cluster_indexes = np.argsort(np.sum(centers, axis=1))
    
    priority_mapping = {
        sorted_cluster_indexes[0]: "MONITOR",
        sorted_cluster_indexes[1]: "SHORT TERM",
        sorted_cluster_indexes[2]: "IMMEDIATE"
    }
    
    for i, village in enumerate(processed_villages):
        raw_cluster = cluster_labels[i]
        village['ml_cluster_priority'] = priority_mapping[raw_cluster]
        
    return processed_villages

# --- HACKATHON SPATIAL DATA INTEGRATION ---
if __name__ == "__main__":
    # Mock dataset containing real-world coordinate structures (Latitude & Longitude)
    spatial_dataset = [
        {"name": "Village Alpha", "lat": 25.612, "lon": 85.137, "rainfall_mm": 380, "slope_deg": 52, "population": 2800, "road_access": "poor"},
        {"name": "Village Beta", "lat": 25.620, "lon": 85.145, "rainfall_mm": 120, "slope_deg": 8,  "population": 350,  "road_access": "good"},
        {"name": "Village Gamma", "lat": 25.605, "lon": 85.120, "rainfall_mm": 290, "slope_deg": 35, "population": 1200, "road_access": "moderate"},
        {"name": "Village Delta", "lat": 25.635, "lon": 85.160, "rainfall_mm": 410, "slope_deg": 48, "population": 1900, "road_access": "poor"},
        {"name": "Village Epsilon", "lat": 25.590, "lon": 85.105, "rainfall_mm": 90,  "slope_deg": 4,  "population": 150,  "road_access": "good"},
    ]
    
    # Run the ML system
    final_output = cluster_village_risks(spatial_dataset)
    
    # Print results to console to verify
    print("\n--- ML Spatial Triage Summary ---")
    for v in final_output:
        print(f"{v['name']} ({v['lat']}, {v['lon']}) -> Priority: {v['ml_cluster_priority']} (Risk Score: {v['risk_score']})")
        
    # Automatically export to a JSON file so the Backend/GIS team can read it instantly
    output_filename = "villages_output.json"
    with open(output_filename, "w") as f:
        json.dump(final_output, f, indent=4)
        
    print(f"\n[SUCCESS] Saved spatial results to {output_filename}")
