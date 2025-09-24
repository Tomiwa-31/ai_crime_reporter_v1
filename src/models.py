from extensions import db
from datetime import datetime

class CrimeReport(db.Model):
    """Model for storing processed crime reports"""
    __tablename__ = 'crime_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    predicted_label = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False, default=0.0)
    trust_score = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CrimeReport {self.id}: {self.category} at ({self.latitude}, {self.longitude})>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'original_text': self.original_text,
            'predicted_label': self.predicted_label,
            'confidence': self.confidence,
            'trust_score': self.trust_score,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'category': self.category,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
