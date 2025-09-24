import requests
import os

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")

def get_coordinates_from_text(location_text: str):
    """Extract coordinates from text using Mapbox API"""
    if not MAPBOX_TOKEN:
        print("⚠️ MAPBOX_TOKEN not found in environment variables")
        return None
    
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location_text}.json"
    params = {
        "access_token": MAPBOX_TOKEN,
        "limit": 1,
        "types": "poi,place,address"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "features" in data and len(data["features"]) > 0:
            coords = data["features"][0]["geometry"]["coordinates"]
            return (coords[1], coords[0])  # (lat, lon)
        
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None
