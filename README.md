# Credit Default Prediction Pipeline

Automated ML pipeline for credit default prediction (PD model).

## Project Description

This project implements an end-to-end automated pipeline for development, testing, deployment and monitoring of machine learning models for predicting client default probability.

**Domain:** Finance / Credit Scoring  
**Dataset:** Default of Credit Card Clients Dataset from UCI Machine Learning Repository

## Project Structure

`
â”œâ”€â”€ data/                   # Data (raw, processed)
â”œâ”€â”€ models/                 # Trained models
â”œâ”€â”€ notebooks/              # Jupyter notebooks for EDA
â”œâ”€â”€ src/                    # Source code
â”‚   â”œâ”€â”€ data/              # Data processing modules
â”‚   â”œâ”€â”€ models/            # Model training modules
â”‚   â”œâ”€â”€ api/               # FastAPI application
â”‚   â””â”€â”€ monitoring/        # Monitoring modules
â”œâ”€â”€ tests/                  # Tests
â”œâ”€â”€ scripts/                # Run scripts
â”œâ”€â”€ .github/workflows/      # GitHub Actions
â”œâ”€â”€ dvc.yaml               # DVC pipeline
â”œâ”€â”€ Dockerfile             # Docker configuration
â””â”€â”€ requirements.txt       # Dependencies
`

## Installation and Setup

### 1. Clone Repository
`ash
git clone https://github.com/sstanna/credit-default-prediction.git
cd credit-default-prediction
`

### 2. Install Dependencies
`ash
pip install -r requirements.txt
`

### 3. Prepare Data
`ash
python -m src.data.load_data
`

### 4. Train Model
`ash
python scripts/train_models.py
`

### 5. Run API
`ash
python scripts/run_api.py
# or
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
`

### 6. Run Tests
`ash
pytest tests/ -v
`

### 7. Monitor Drift
`ash
python scripts/monitor_drift.py
`

### 8. Docker Run
`ash
docker build -t credit-default-api .
docker run -p 8000:8000 credit-default-api
`

## Project Components

### 1. Data Preparation and Validation
- Data loading from UCI ML Repository
- Feature Engineering (aggregated features, binning)
- Validation with Great Expectations

### 2. Model Training
- Sklearn Pipeline with preprocessing
- Automatic hyperparameter tuning
- Metrics: ROC-AUC, Precision, Recall, F1-Score

### 3. Experimentation
- MLflow Tracking for experiment logging
- Model and data versioning with DVC

### 4. Testing and CI/CD
- Unit tests with pytest
- GitHub Actions for automated testing
- Linting with flake8 and formatting with black

### 5. Deployment
- FastAPI REST API
- Docker containerization
- Data drift monitoring

## API Endpoints

- GET / - API information
- POST /predict - Default prediction
- GET /health - Health check
- POST /predict_batch - Batch prediction
- GET /model_info - Model information

## API Usage Example

`python
import requests

url = "http://localhost:8000/predict"
data = {
    "LIMIT_BAL": 20000,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 1,
    "AGE": 24,
    "PAY_0": 2,
    "PAY_2": 2,
    "PAY_3": -1,
    "PAY_4": -1,
    "PAY_5": -2,
    "PAY_6": -2,
    "BILL_AMT1": 3913,
    "BILL_AMT2": 3102,
    "BILL_AMT3": 689,
    "BILL_AMT4": 0,
    "BILL_AMT5": 0,
    "BILL_AMT6": 0,
    "PAY_AMT1": 0,
    "PAY_AMT2": 689,
    "PAY_AMT3": 0,
    "PAY_AMT4": 0,
    "PAY_AMT5": 0,
    "PAY_AMT6": 0
}

response = requests.post(url, json=data)
print(response.json())
`

## Monitoring

Script src/monitoring/drift_monitor.py tracks data drift and calculates Population Stability Index (PSI).

`python
from src.monitoring.drift_monitor import DataDriftMonitor

monitor = DataDriftMonitor(reference_data)
report = monitor.generate_drift_report(new_data)
`

## MLflow Tracking

Start MLflow UI:
`ash
mlflow ui
`

Open http://localhost:5000 in browser to view experiments.

## DVC Pipeline

Run pipeline:
`ash
dvc repro
`

## Testing

Run all tests:
`ash
pytest tests/ -v --cov=src
`

Run linting:
`ash
flake8 src tests
black src tests
`

## Results

- **Dataset:** 30,000 records successfully processed
- **Target variable:** 22.12% defaults (6,636 out of 30,000)
- **Feature Engineering:** 4 new features created
- **Models:** 3 algorithms trained with hyperparameters
- **API:** REST API ready for production use
- **Monitoring:** PSI drift detector implemented

## Author

ML Engineer - Credit Department (sstanna)

## License

MIT License
