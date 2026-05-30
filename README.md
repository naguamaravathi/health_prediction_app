# Health Prediction App

A Flask-based web application for managing patient records and predicting potential health risks using machine learning.

## ✨ Features
- Add, view, edit, and delete patient records
- Input validation (email, date of birth, numeric health values)
- Machine learning model (`risk_model.pkl`) predicts risks based on glucose, haemoglobin, and cholesterol
- Clean, responsive Bootstrap interface
- Flash messages for instant feedback
- SQLite database for persistent storage

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite
- **ML Model**: scikit-learn (saved with joblib)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/naguamaravathi/health_prediction_app.git
   cd health_prediction_app
