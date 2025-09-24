import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
load_dotenv()  # This loads variables from .env file into environment
# Import AI components only if available
try:
    from langgraph.graph import StateGraph, END
    from langgraph_nodes import AlertFilterState, user_input_node, validation_node, geo_verification_node
    AI_ENABLED = True
except ImportError:
    print("⚠️ AI components not available, running in basic mode")
    AI_ENABLED = False
# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Import db from extensions instead of creating it  to avoid import error of being stick in a loop
from extensions import db

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
#app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Build LangGraph workflow if AI components available
if AI_ENABLED:
    graph_builder = StateGraph(AlertFilterState)
    graph_builder.add_node("user_input", user_input_node)
    graph_builder.add_node("validation", validation_node)
    graph_builder.add_node("geo_verification", geo_verification_node)

    graph_builder.set_entry_point("user_input")
    graph_builder.add_edge("user_input", "validation")
    graph_builder.add_edge("validation", "geo_verification")
    graph_builder.add_edge("geo_verification", END)

    app_graph = graph_builder.compile()#eturns a compiled graph object almost similar to a dictionary containg nides,edes and other metadata
else:
    app_graph = None

with app.app_context():
    # Import models here so their tables are created
    from models import CrimeReport
    db.create_all()

def calculate_stats(reports):
    """Calculate statistics from crime reports for the dashboard"""
    stats = {}
    for report in reports:
        category = report.category or "Unknown"
        stats[category] = stats.get(category, 0) + 1
    return stats

@app.route('/')
def home():
    """Main dashboard route - serves the complete dashboard with data"""
    try:
        # Query verified reports (trust score > 0.5)
        verified_reports = CrimeReport.query.filter(
            CrimeReport.trust_score > 0.5
        ).order_by(CrimeReport.timestamp.desc()).limit(50).all()
        
        # Calculate statistics for the chart
        stats = calculate_stats(verified_reports)
        
        # Get recent alerts for the sidebar (last 10)
        recent_alerts = CrimeReport.query.filter(
            CrimeReport.trust_score > 0.5
        ).order_by(CrimeReport.timestamp.desc()).limit(10).all()
        
        # Convert reports to dictionaries for JSON serialization
        reports_dict = [report.to_dict() for report in verified_reports]
        
        app.logger.info(f"Loaded {len(verified_reports)} verified reports")
        app.logger.info(f"Statistics: {stats}")
        
        return render_template('index.html', 
                             reports=reports_dict, 
                             statistics=stats,
                             recent_alerts=recent_alerts)
    
    except Exception as e:
        app.logger.error(f"Error loading dashboard: {str(e)}")
        flash(f"Error loading dashboard: {str(e)}", "error")
        return render_template('index.html', 
                             reports=[], 
                             statistics={},
                             recent_alerts=[])

@app.route('/api/process', methods=['POST'])
def process_alert():
    """Process crime report through AI pipeline and save to database"""
    try:
        data = request.get_json()
        user_report = data.get('report', '')
        user_lat = data.get('latitude', 0.0)
        user_lng = data.get('longitude', 0.0)
        
        if not user_report:
            return jsonify({"error": "No report provided"}), 400
        
        app.logger.info(f"Processing report: {user_report[:100]}...")
        
        # Initialize state with user GPS location if provided
        initial_state = {
            "user_report": user_report,
            "trust_score": 1.0,
            "gps_location": (user_lat, user_lng) if user_lat and user_lng else (0.0, 0.0),
            "alert_type": ""
        }
        
        # Process through AI workflow if available, otherwise use fallback
        if AI_ENABLED and app_graph:
            result = app_graph.invoke(initial_state)
        else:
            # Simple fallback processing without AI
            result = {
                'user_report': user_report,
                'trust_score': 0.8,  # Default trust score
                'gps_location': (user_lat, user_lng) if user_lat and user_lng else (6.6018, 3.3515),  # Lagos default
                'alert_type': 'Crime Report'  # Generic category
            }
        
        # Save to database if trust score is decent
        if result.get('trust_score', 0) > 0.3:
            crime_report = CrimeReport(
                original_text=user_report,
                predicted_label=result.get('alert_type', 'unknown'),
                confidence=0.8,  # This would come from the model in a real scenario
                trust_score=result.get('trust_score', 0),
                latitude=result['gps_location'][0],
                longitude=result['gps_location'][1],
                category=result.get('alert_type', 'Unknown').title(),
                timestamp=datetime.utcnow()
            )
            
            db.session.add(crime_report)
            db.session.commit()
            
            app.logger.info(f"Saved crime report with ID: {crime_report.id}")
            
            return jsonify({
                "success": True,
                "message": "Report processed and saved successfully",
                "result": result,
                "report_id": crime_report.id
            })
        else:
            app.logger.info("Report rejected due to low trust score")
            return jsonify({
                "success": False,
                "message": "Report could not be verified",
                "result": result
            })
        
    except Exception as e:
        app.logger.error(f"Error processing alert: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports')
def get_reports():
    """API endpoint to get all verified reports (for AJAX if needed)"""
    try:
        verified_reports = CrimeReport.query.filter(
            CrimeReport.trust_score > 0.5
        ).order_by(CrimeReport.timestamp.desc()).all()
        
        reports_data = []
        for report in verified_reports:
            reports_data.append({
                'id': report.id,
                'latitude': report.latitude,
                'longitude': report.longitude,
                'category': report.category,
                'trust_score': report.trust_score,
                'timestamp': report.timestamp.isoformat(),
                'original_text': report.original_text[:100] + '...' if len(report.original_text) > 100 else report.original_text
            })
        
        return jsonify(reports_data)
    
    except Exception as e:
        app.logger.error(f"Error fetching reports: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
