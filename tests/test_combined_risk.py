import pytest
import json
from unittest.mock import patch
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.config import logger

@pytest.fixture
def client():
    app = create_app(testing=True) 
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def mock_api_response(url, json, *args, **kwargs):
    """Mock response for external API calls."""
    if "price/risk" in url:
        return MockResponse({"predicted_price": 20000, "predicted_risk_score": 10}, 200)
    elif "spare-parts/risk" in url:
        return MockResponse({"predicted_spare_parts_risk_percentage": 5.5}, 200)
    elif "insurance/risk" in url:
        return MockResponse({"risk_rank": 50}, 200)
    elif "insurance/explanation" in url:
        return MockResponse({
            "explanation": "Your premium is stable due to market consistency.",
            "total_risk_score": 12,
            "adjusted_premium": 2500,
            "adjustment_factor": 5
        }, 200)
    return MockResponse({}, 404)

class MockResponse:
    """Custom mock response class to mimic requests.Response"""
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    def json(self):
        return self.json_data

@patch('requests.post', side_effect=mock_api_response)
def test_combined_risk_success(mock_post, client):
    """Test successful risk prediction with mock API responses."""
    test_data = {
        "make": "Toyota",
        "model": "Allion",
        "vehicle_type": "Car",
        "year": 2018,
        "mileage": 55000
    }
    
    response = client.post('/api/vehicles/risk', data=json.dumps(test_data), content_type='application/json')
    
    assert response.status_code == 200
    response_data = response.json

    assert "predicted_price" in response_data
    assert "predicted_market_risk_score" in response_data
    assert "predicted_spare_parts_risk_percentage" in response_data
    assert "predicted_claim_risk_rank" in response_data
    assert "explanation" in response_data
    assert "total_risk_score" in response_data
    assert "premium_adjustment" in response_data
    assert "premium_adjustment_percentage" in response_data

@patch('requests.post', return_value=MockResponse({"error": "Invalid input"}, 400))
def test_combined_risk_invalid_input(mock_post, client):
    """Test API response for invalid input."""
    test_data = {
        "make": "Toyota",
        "model": "Corolla"
    }

    response = client.post('/api/vehicles/risk', data=json.dumps(test_data), content_type='application/json')

    assert response.status_code == 400
    assert "error" in response.json

@patch('requests.post', return_value=MockResponse({"error": "Service unavailable"}, 500))
def test_combined_risk_external_api_failure(mock_post, client):
    """Test API response when external service fails."""
    test_data = {
        "make": "Toyota",
        "model": "Corolla",
        "vehicle_type": "Car",
        "year": 2020,
        "mileage": 30000
    }

    response = client.post('/api/vehicles/risk', data=json.dumps(test_data), content_type='application/json')

    assert response.status_code == 500
    assert "error" in response.json

@patch('requests.post', return_value=MockResponse({}, 404))
def test_combined_risk_external_api_not_found(mock_post, client):
    """Test API response when external service is not found."""
    test_data = {
        "make": "Toyota",
        "model": "Corolla",
        "vehicle_type": "Car",
        "year": 2020,
        "mileage": 30000
    }

    response = client.post('/api/vehicles/risk', data=json.dumps(test_data), content_type='application/json')

    assert response.status_code == 500
    assert "error" in response.json

@patch('requests.post', return_value=MockResponse({"error": "Internal server error"}, 500))
def test_combined_risk_internal_server_error(mock_post, client):
    """Test API response for internal server error."""
    test_data = {
        "make": "Toyota",
        "model": "Corolla",
        "vehicle_type": "Car",
        "year": 2020,
        "mileage": 30000
    }

    response = client.post('/api/vehicles/risk', data=json.dumps(test_data), content_type='application/json')

    assert response.status_code == 500
    assert "error" in response.json

@patch('requests.post', return_value=MockResponse({"error": "Unauthorized access"}, 401))
def test_combined_risk_unauthorized_access(mock_post, client):
    """Test API response for unauthorized access."""
    test_data = {
        "make": "Toyota",
        "model": "Corolla",
        "vehicle_type": "Car",
        "year": 2020,
        "mileage": 30000
    }

    response = client.post('/api/vehicles/risk', data=json.dumps(test_data), content_type='application/json')

    assert response.status_code == 401
    assert "error" in response.json

