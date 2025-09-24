
from flask import Flask, request, jsonify, render_template
from langgraph.graph import StateGraph, END
from langgraph_nodes import AlertFilterState, user_input_node, validation_node, geo_verification_node
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Build LangGraph workflow
graph_builder = StateGraph(AlertFilterState)
graph_builder.add_node("user_input", user_input_node)
graph_builder.add_node("validation", validation_node)
graph_builder.add_node("geo_verification", geo_verification_node)

graph_builder.set_entry_point("user_input")
graph_builder.add_edge("user_input", "validation")
graph_builder.add_edge("validation", "geo_verification")
graph_builder.add_edge("geo_verification", END)

app_graph = graph_builder.compile()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_alert():
    try:
        data = request.get_json()
        user_report = data.get('report', '')
        
        if not user_report:
            return jsonify({"error": "No report provided"}), 400
        
        # Initialize state
        initial_state = {
            "user_report": user_report,
            "trust_score": 1.0,
            "gps_location": (0.0, 0.0),  # Will be overwritten
            "alert_type": ""
        }
        
        # Process through LangGraph
        result = app_graph.invoke(initial_state)
        
        return jsonify({
            "success": True,
            "result": result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)