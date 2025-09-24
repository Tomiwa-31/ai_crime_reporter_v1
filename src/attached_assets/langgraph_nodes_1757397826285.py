
from typing import Tuple, Union, TypedDict
from geopy.distance import geodesic
from model_utils import model_classifier
from geo_utils import get_coordinates_from_text

class AlertFilterState(TypedDict):
    user_report: str
    trust_score: Union[float, int]
    gps_location: Tuple[float, float]
    alert_type: str

def user_input_node(state: AlertFilterState):
    """Extract location from user report text"""
    report_text = state["user_report"]
    extracted_coords = get_coordinates_from_text(report_text)
    
    if extracted_coords:
        state["gps_location"] = extracted_coords
        print(f"📍 Extracted coordinates: {extracted_coords}")
    else:
        # Default to Lagos coordinates if extraction fails
        state["gps_location"] = (6.6018, 3.3515)
        print("⚠️ No location found, using default coordinates")
    
    return state

def validation_node(state: AlertFilterState):
    """Classify the report and set initial trust score"""
    result = model_classifier(state['user_report'])
    state['alert_type'] = result['predicted_label']
    state['trust_score'] = result['trust_score']
    return state

def geo_verification_node(state: AlertFilterState):
    """Optional consistency check for location"""
    report_text = state["user_report"]
    extracted_coords = state["gps_location"]
    
    second_extraction = get_coordinates_from_text(report_text)
    if second_extraction:
        distance_km = geodesic(extracted_coords, second_extraction).km
        print(f"🔍 Location consistency: {distance_km:.2f} km difference")
        
        if distance_km > 50:
            print("⚠️ Inconsistent location - penalizing trust")
            state["trust_score"] *= 0.8
    
    return state