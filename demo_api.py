from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import random

# Initialize FastAPI app
app = FastAPI(
    title='Credit Default Prediction API - Demo',
    description='Simplified demo API for predicting credit card default probability',
    version='1.0.0'
)

class CreditCardData(BaseModel):
    LIMIT_BAL: float = Field(..., description='Credit limit balance')
    SEX: int = Field(..., description='Gender (1=male, 2=female)')
    EDUCATION: int = Field(..., description='Education level (1-4)')
    MARRIAGE: int = Field(..., description='Marital status (1-3)')
    AGE: int = Field(..., description='Age in years')
    PAY_0: int = Field(..., description='Payment status in September')
    PAY_2: int = Field(..., description='Payment status in August')
    PAY_3: int = Field(..., description='Payment status in July')
    PAY_4: int = Field(..., description='Payment status in June')
    PAY_5: int = Field(..., description='Payment status in May')
    PAY_6: int = Field(..., description='Payment status in April')
    BILL_AMT1: float = Field(..., description='Bill amount in September')
    BILL_AMT2: float = Field(..., description='Bill amount in August')
    BILL_AMT3: float = Field(..., description='Bill amount in July')
    BILL_AMT4: float = Field(..., description='Bill amount in June')
    BILL_AMT5: float = Field(..., description='Bill amount in May')
    BILL_AMT6: float = Field(..., description='Bill amount in April')
    PAY_AMT1: float = Field(..., description='Payment amount in September')
    PAY_AMT2: float = Field(..., description='Payment amount in August')
    PAY_AMT3: float = Field(..., description='Payment amount in July')
    PAY_AMT4: float = Field(..., description='Payment amount in June')
    PAY_AMT5: float = Field(..., description='Payment amount in May')
    PAY_AMT6: float = Field(..., description='Payment amount in April')

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description='Predicted class (0=no default, 1=default)')
    probability: float = Field(..., description='Probability of default')
    confidence: str = Field(..., description='Confidence level')

def simple_prediction_logic(data: CreditCardData) -> dict:
    risk_score = 0
    
    # Age factor
    if data.AGE < 25:
        risk_score += 0.3
    elif data.AGE > 50:
        risk_score += 0.2
    
    # Payment history factor
    payment_delays = sum([1 for x in [data.PAY_0, data.PAY_2, data.PAY_3, data.PAY_4, data.PAY_5, data.PAY_6] if x > 0])
    risk_score += payment_delays * 0.1
    
    # Credit utilization factor
    avg_bill = (data.BILL_AMT1 + data.BILL_AMT2 + data.BILL_AMT3 + data.BILL_AMT4 + data.BILL_AMT5 + data.BILL_AMT6) / 6
    utilization = avg_bill / (data.LIMIT_BAL + 1)
    if utilization > 0.8:
        risk_score += 0.4
    elif utilization > 0.5:
        risk_score += 0.2
    
    # Education factor
    if data.EDUCATION in [1, 2]:
        risk_score -= 0.1
    
    # Add randomness for demo
    risk_score += random.uniform(-0.1, 0.1)
    
    # Convert to probability
    probability = min(max(risk_score, 0.01), 0.99)
    prediction = 1 if probability > 0.5 else 0
    
    # Determine confidence
    if abs(probability - 0.5) > 0.3:
        confidence = 'high'
    elif abs(probability - 0.5) > 0.15:
        confidence = 'medium'
    else:
        confidence = 'low'
    
    return {
        'prediction': prediction,
        'probability': round(probability, 3),
        'confidence': confidence
    }

@app.get('/')
async def root():
    return {
        'message': 'Credit Default Prediction API - Demo Version',
        'version': '1.0.0',
        'status': 'running',
        'description': 'This is a simplified demo version that works without ML dependencies'
    }

@app.get('/health')
async def health_check():
    return {
        'status': 'healthy',
        'model_loaded': True,
        'demo_mode': True
    }

@app.post('/predict', response_model=PredictionResponse)
async def predict_default(data: CreditCardData):
    try:
        result = simple_prediction_logic(data)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Prediction failed: {str(e)}')

@app.get('/model_info')
async def get_model_info():
    return {
        'model_type': 'Business Rules Engine (Demo)',
        'model_loaded': True,
        'demo_mode': True,
        'description': 'This demo uses business rules instead of ML model due to dependency issues'
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
