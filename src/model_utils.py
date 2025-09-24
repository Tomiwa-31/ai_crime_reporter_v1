import os

# Try to import AI libraries, fallback if not available
try:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    AI_LIBS_AVAILABLE = True
except ImportError:
    print("⚠️ AI libraries (torch, transformers) not available")
    AI_LIBS_AVAILABLE = False

# Load model from Hugging Face Hub
MODEL_NAME = "toladimeji/bert_crime_alert_classifier"

# Load once when module is imported
if AI_LIBS_AVAILABLE:
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=os.getenv("HUGGINGFACE_TOKEN"))
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, token=os.getenv("HUGGINGFACE_TOKEN"))
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"⚠️ Error loading model: {e}")
        # Fallback to a basic model or create dummy responses
        tokenizer = None
        model = None
else:
    tokenizer = None
    model = None

def model_classifier(text):
    """Classify text and return results with trust score"""
    if not model or not tokenizer:
        # Fallback classification when model is not available
        return {
            "original_text": text,
            "predicted_label": "real" if "robbery" in text.lower() or "theft" in text.lower() or "assault" in text.lower() else "fake",
            "confidence": 0.7,
            "trust_score": 0.6
        }
    
    try:
        if AI_LIBS_AVAILABLE:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            
            with torch.no_grad():
                outputs = model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        else:
            # Fallback when AI libraries not available
            return {
                "original_text": text,
                "predicted_label": "real" if any(word in text.lower() for word in ["robbery", "theft", "assault", "crime"]) else "unknown",
                "confidence": 0.7,
                "trust_score": 0.6
            }
        
        predicted_class_id = predictions.argmax().item()
        confidence_score = predictions[0][predicted_class_id].item()
        
        # Check your model's actual labels - adjust this mapping!
        label_mapping = {0: "fake", 1: "real"}  # Update based on your model
        
        predicted_label = label_mapping.get(predicted_class_id, "unknown")
        
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
    
    except Exception as e:
        print(f"Error in model classification: {e}")
        # Return fallback result
        return {
            "original_text": text,
            "predicted_label": "unknown",
            "confidence": 0.5,
            "trust_score": 0.5
        }
