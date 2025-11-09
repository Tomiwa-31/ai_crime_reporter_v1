Data Collection & Preparation
Step 1: Dataset Acquisition
o	Used a custom crime dataset with text reports and binary labels
o	Total samples split into:
	Training: (70%)
	Validation: (15%)
	Test: (15%)
o	Binary Classification: "fake" (0) vs "real" (1) crime reports
Step 2: Data Preprocessing
o	Stratified train-test-validation split to maintain label distribution
o	 to Hugging Face DatasetDict format for efficient processing
o	Label mapping: {"fake": 0, "real": 1} for model compatibility
Model Development
Step 3: Model Selection & Setup
•	Base Model: google-bert/bert-base-uncased (pre-trained)
•	Task: Sequence classification for fake/real crime report detection
•	Transfer Learning Approach: Fine-tuned BERT on crime dataset
Step 4: Strategic Model Freezing
•	Frozen Layers: All BERT encoder layers (preserving pre-trained knowledge)
•	Trainable Layers:
o	BERT pooler layer
o	Final classifier layer
•	Benefits: Faster training, less overfitting, efficient computation
Step 5: Training Configuration
•	Learning Rate: 2e-4
•	Batch Size: 8
•	Epochs: 10
•	Evaluation Metrics: Accuracy + ROC AUC
•	Training Strategy: Epoch-based logging and evaluation
•	
Model Performance & Evaluation
Evaluation Metrics:
•	Accuracy: Measured classification correctness
•	ROC AUC: Assessed model's ability to distinguish between fake/real reports
•	Final Training Loss: 0.093 (indicating good convergence)

LangGraph Workflow Breakdown
Step 1: Location Intelligence (user_input_node)
•	GPS Priority: Uses provided coordinates when available
•	Text Extraction: Falls back to geo_utils.get_coordinates_from_text() for location parsing
Step 2: AI Classification (validation_node)
•	Model Integration: Calls model_classifier() with user report
•	Dual Output: Returns both predicted_label and trust_score
•	Real-time Processing: Immediate classification of crime reports
•	Confidence Scoring: Generates trust scores (0.0-1.0) for credibility assessment
Step 3: Geographic Verification (geo_verification_node)
•	Consistency Check: Compares extracted locations from text
•	Distance Validation: Uses geodesic for accurate distance calculation
•	Trust Adjustment: Penalizes inconsistent reports (>50km difference)
•	Smart Skipping: Bypasses verification for default coordinates
Flask Integration Summary
 Core Architecture
•	Flask Backend with SQLAlchemy ORM and SQLite database
•	Modular AI Integration - LangGraph workflows embedded directly in routes
•	Production Configuration - environment variables, connection pooling, secure sessions
 Integration Achievements
Seamless AI-Backend Integration
•	LangGraph workflows directly embedded in Flask routes
•	app_graph.invoke() calls AI pipeline from within API endpoints
•	Graceful fallback when AI components unavailable
 Real-time Data Processing
•	Instant AI analysis via /api/process endpoint
•	BERT classification + trust scoring in milliseconds
•	Live geographic verification and consistency checks
Intelligent Filtering
•	Storage threshold: Only saves reports with >30% trust score
•	Display threshold: Only shows reports with >50% trust score
•	Real-time statistics calculation from verified data
Production Resilience
•	Comprehensive error handling with detailed logging
•	Environment-based configuration management
•	Database connection pooling and health checks
•	Graceful degradation without AI components
RESTful API Design
•	Clean JSON endpoints: /api/process (POST) and /api/reports (GET)
•	Standard HTTP status codes and error responses
•	Frontend-backend communication via JSON serialization
Database Optimization
•	Efficient queries with trust-based filtering
•	SQLite with connection pooling for production readiness
•	Automatic schema creation and migration handling
•	Optimized data serialization for dashboard displa
Deployment Stage
•	Final deployment was achieved using Docker containerization on Hugging Face Spaces. The application was packaged with a minimal Dockerfile and successfully deployed to Hugging Face's cloud platform.
•	Platform: Hugging Face Spaces
URL: hf.co/spaces/toladimeji/crime_ai_reporter_v2
















