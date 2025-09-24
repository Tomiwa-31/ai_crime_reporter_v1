# Crime Alert Dashboard

## Overview

A Flask-based AI-powered crime reporting and monitoring system that processes user-submitted crime reports through machine learning classification, geocoding, and trust scoring. The application provides a comprehensive dashboard with an interactive map, real-time statistics, and verified incident tracking. It uses LangGraph for workflow orchestration, combining natural language processing, geographical verification, and data visualization to create a complete crime monitoring solution.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM for database operations
- **Workflow Engine**: LangGraph state machine for processing crime reports through multiple validation stages
- **AI Classification**: Hugging Face BERT model (`toladimeji/bert_crime_alert_classifier`) for distinguishing real vs fake crime reports
- **Database**: MySQL with PyMySQL connector for storing processed crime reports
- **State Management**: TypedDict-based state objects for workflow consistency

### AI Processing Pipeline
- **Three-Stage Workflow**: User input processing, ML validation, and geographical verification
- **Trust Scoring**: Dynamic scoring system based on AI confidence and location consistency
- **Geocoding**: Mapbox API integration for converting text descriptions to coordinates
- **Fallback Logic**: Default coordinates (Lagos, Nigeria) when location extraction fails

### Frontend Architecture
- **Template Engine**: Jinja2 for server-side rendering with data injection
- **Interactive Map**: Leaflet.js for crime incident visualization
- **Statistics**: Chart.js for real-time crime category breakdowns
- **Responsive Design**: Bootstrap with dark theme support
- **Progressive Enhancement**: Core functionality works without JavaScript, enhanced with client-side features

### Data Storage
- **Primary Model**: CrimeReport with fields for original text, AI predictions, confidence scores, coordinates, and timestamps
- **Filtering Logic**: Only reports with trust scores > 0.5 are displayed on the dashboard
- **Real-time Updates**: Direct database queries feed into template rendering

### Security & Configuration
- **Environment Variables**: Secure handling of API tokens (Mapbox, Hugging Face)
- **Proxy Support**: ProxyFix middleware for proper header handling in deployment environments
- **Session Management**: Flask secret key configuration for secure sessions

## External Dependencies

### AI/ML Services
- **Hugging Face Hub**: BERT model hosting and tokenization services
- **PyTorch**: Machine learning inference engine
- **Transformers**: Natural language processing library

### Geocoding & Mapping
- **Mapbox API**: Geocoding service for converting text to coordinates
- **Leaflet.js**: Open-source mapping library for interactive crime visualization
- **OpenStreetMap**: Tile layer provider for map rendering

### Database & Infrastructure
- **MySQL**: Primary database for crime report storage
- **SQLAlchemy**: ORM for database operations and model management
- **PyMySQL**: Python MySQL connector

### Geospatial Computing
- **GeoPy**: Distance calculations for location consistency verification
- **Geodesic**: Earth surface distance measurements

### Frontend Libraries
- **Bootstrap**: UI component framework with dark theme
- **Chart.js**: Statistical data visualization
- **Font Awesome**: Icon library for dashboard UI

### Development & Configuration
- **python-dotenv**: Environment variable management
- **Flask Extensions**: SQLAlchemy integration and request handling
- **Werkzeug**: WSGI utilities and middleware support