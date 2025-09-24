
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from dotenv import load_dotenv
import os

load_dotenv()

# Load model from Hugging Face Hub (NO need to pickle!)
MODEL_NAME = "toladimeji/bert_crime_alert_classifier"

# Load once when module is imported
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def model_classifier(text):
    """Classify text and return results with trust score"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    predicted_class_id = predictions.argmax().item()
    confidence_score = predictions[0][predicted_class_id].item()
    
    # Check your model's actual labels - adjust this mapping!
    label_mapping = {0: "fake", 1: "real"}  # Update based on your model
    
    predicted_label = label_mapping[predicted_class_id]
    
    if predicted_label == "fake":
        trust_score = 0.2 * confidence_score
    elif predicted_label == "real":
        trust_score = 0.8 * confidence_score
    else:
        trust_score = 0.5
    
    return {
        "original_text": text,
        "predicted_label": predicted_label,
        "confidence": confidence_score,
        "trust_score": trust_score
    }