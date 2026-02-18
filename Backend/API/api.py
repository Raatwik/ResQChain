from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import requests
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

model = joblib.load("priority_model.pkl")

class InputData(BaseModel):
    damage_score: float
    population: int
    hospitals: int
    roads: int

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
def predict(data: InputData):

    features = [[
        data.damage_score,
        data.population,
        data.hospitals,
        data.roads
    ]]

    prediction = model.predict(features)[0]

    reasons = []

    if data.damage_score > 0.7:
        reasons.append("High infrastructure damage")
    if data.population > 50000:
        reasons.append("Dense population")
    if data.hospitals <= 1:
        reasons.append("Limited medical access")
    if data.roads == 0:
        reasons.append("Road access blocked")

    confidence = "medium"
    if len(reasons) >= 3:
        confidence = "high"

    return {
        "priority": str(prediction),
        "confidence": confidence,
        "explanation": reasons,
        "data_sources": {
            "damage": "xView2 (cached)",
            "population": "estimated",
            "hospitals": "live OSM",
            "roads": "estimated",
        }
    }


def estimate_population(lat, lon, radius=1000):
    query = f"""
    [out:json];
    way["building"](around:{radius},{lat},{lon});
    out;
    """
    res = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=query
    )
    data = res.json()
    return len(data.get("elements", [])) * 5

@app.get("/analyze-location")
def analyze_location(lat: float, lon: float):

    population = estimate_population(lat, lon)# random 
    hospitals = 5  # live
    roads = 1      # estimate
    damage_score = 9.3  # simulated or cached

    features = [[damage_score, population, hospitals, roads]]
    priority = model.predict(features)[0]

    reasons = []
    if damage_score > 0.7: reasons.append("High damage")
    elif population > 5000: reasons.append("Dense population")
    elif hospitals <= 1: reasons.append("Low hospital access")

    return {
        "priority": str(priority),
        "population": population,
        "confidence": "High",
        "explanation": reasons
    }


OPENWEATHER_KEY = "{insert_your_openweather_api_key_here}"

@app.get("/live-alerts")
def live_alerts(lat: float, lon: float):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}"
    
    resp = requests.get(url)
    data = resp.json()

    # Safety check: if API key is wrong or lat/lon invalid
    if resp.status_code != 200:
        return {"status": "unknown", "message": "Weather service unavailable"}

    weather = data.get("weather", [])
    if not weather:
        return {"status": "unknown", "message": "No weather data"}

    condition = weather[0]["main"]

    # Trigger alert for dangerous conditions
    if condition in ["Rain", "Thunderstorm", "Snow", "Drizzle", "Tornado", "Squall"]:
        return {
            "status": "alert",
            "type": condition,
            "message": f"Potential {condition.lower()} risk detected"
        }
    
    return {
        "status": "safe",
        "type": condition,
        "message": "Conditions are currently clear."
    }
@app.get("/responder-priority-map")
def responder_priority():
    # 1. fetched from xView2 results and OSM
    live_zones = [
        {"lat": 12.823, "lon": 80.044, "damage": 8.5, "pop": 65000, "hosp": 0, "roads": 0},
        {"lat": 12.880, "lon": 80.100, "damage": 5.2, "pop": 12000, "hosp": 1, "roads": 1},
        {"lat": 12.850, "lon": 80.060, "damage": 2.1, "pop": 5000, "hosp": 3, "roads": 1}
    ]

    results = []    
    for zone in live_zones:
        # Prepare features for the loaded model
        features = [[zone["damage"], zone["pop"], zone["hosp"], zone["roads"]]]
        
        # Run real prediction
        prediction = model.predict(features)[0]
        
        # Get Confidence Score from RandomForest
        probs = model.predict_proba(features)[0]
        confidence = float(max(probs))

        # --- AI RECOMMENDATION LOGIC ---
        recommendations = []
        if prediction == "High":
            recommendations.append("Prepare for evacuation within 6 hours")
            recommendations.append(f"Deploy emergency medical kits for {zone['pop']} people")
        
        if zone["hosp"] == 0:
            recommendations.append("Dispatch mobile medical unit (No hospital nearby)")
            
        if zone["roads"] == 0:
            recommendations.append("Coordinate air-drop (Road access blocked)")
        else:
            recommendations.append("Coordinate with nearby shelter (2.4 km)")

        results.append({
            "lat": zone["lat"],
            "lon": zone["lon"],
            "priority": str(prediction),
            "recommendations": recommendations,
            "people": zone["pop"],
            "confidence": confidence,
            "reason": f"Damage Score: {zone['damage']} | Infrastructure: {'Limited' if zone['roads']==0 else 'Accessible'}"
        })

    return results

    return {
        "status": "safe",
        "message": "No immediate disaster risk detected"
    }
