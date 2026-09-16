# API Contract: Risk Engine (Module 2 & 3)

**Owner:** ML / Risk Engineer (Person 3)  
**Status:** Ready for Integration  

## Function to Import
The backend can import the baseline function directly from the risk script:
```python
from risk_engine import calculate_village_status
```

## Input Parameters
The function accepts the following variables:

| Parameter Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `rainfall_mm` | `float` / `int` | Current or simulated scenario rainfall | `350` |
| `slope_deg` | `float` / `int` | Topographic slope angle of the area | `45` |
| `population` | `int` | Total headcount exposed in the village | `2500` |
| `road_access` | `string` | Quality of local road infrastructure | `"poor"`, `"moderate"`, `"good"` |

## Output Format (JSON / Dictionary)
The function returns a structured dictionary matching this exact schema:

```json
{
  "risk_score": 0.72,
  "is_red_zone": true,
  "priority": "IMMEDIATE"
}
```

## Example Backend Usage (FastAPI Route Example)
```python
@app.post("/api/v1/evaluate-village")
def evaluate_village(data: dict):
    # Pass inputs directly to the risk engine
    result = calculate_village_status(
        rainfall_mm=data["rainfall_mm"],
        slope_deg=data["slope_deg"],
        population=data["population"],
        road_access=data["road_access"]
    )
    return result
```
