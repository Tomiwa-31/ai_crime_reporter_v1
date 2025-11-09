AI Crime Reporter with LangGraph

An intelligent crime reporting system that uses AI to verify and classify crime reports in real-time. Built with LangGraph, BERT, and Flask, deployed on Hugging Face Spaces.

 Features
AI-Powered Verification: BERT model classifies reports as real/fake with trust scoring

Multi-Source Geolocation: GPS coordinates + text-based location extraction

Real-time Dashboard: Interactive map with live crime statistics

Intelligent Filtering: Trust-based report validation and display

Production-Ready: Full-stack application with robust error handling

🏗️ System Architecture

Data & Model Pipeline
Dataset: 220 crime reports (70% train, 15% validation, 15% test)

Base Model: google-bert/bert-base-uncased fine-tuned for binary classification

Strategic Freezing: Only pooler and classifier layers trained

Training: 10 epochs, 2e-4 learning rate, 8 batch size

Performance: 0.093 final loss with Accuracy + ROC AUC metrics

LangGraph Workflow

Location Intelligence: GPS priority with text extraction fallback

AI Classification: BERT model predicts label + trust score

Geographic Verification: Consistency checks with distance validation

Flask Integration
Seamless AI Integration: LangGraph workflows embedded in Flask routes

Real-time Processing: Instant analysis via /api/process endpoint

Intelligent Filtering: >30% trust for storage, >50% for display

RESTful API: Clean JSON endpoints with proper error handling

Database Optimization: SQLite with connection pooling and efficient queries

🚀 Deployment
Platform: Hugging Face Spaces
URL: hf.co/spaces/toladimeji/crime_ai_reporter_v2

Final deployment achieved using Docker containerization on Hugging Face Spaces, making the AI crime reporter publicly accessible worldwide.

💻 Technology Stack
Backend: Flask, SQLAlchemy, SQLite

AI/ML: LangGraph, Transformers, BERT

Frontend: HTML, JavaScript, Bootstrap, Leaflet.js

Deployment: Docker, Hugging Face Spaces

Geolocation: Browser Geolocation API, Geopy

📊 Key Achievements
Seamless AI-Backend Integration - LangGraph workflows in Flask routes

Real-time Data Processing - Instant AI analysis with trust scoring

Intelligent Filtering - Multi-level trust-based validation

Production Resilience - Comprehensive error handling and logging

RESTful API Design - Clean JSON endpoints for frontend communication

Database Optimization - Efficient queries with connection pooling
