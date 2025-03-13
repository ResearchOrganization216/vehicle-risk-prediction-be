import os
import logging
import pickle
import xgboost as xgb
import google.generativeai as genai
from app.utils.customer_risk_assesment.risk_assesment_utils import load_xgboost_model, get_feature_importance, format_importance_for_prompt, MODEL_PATH

# Configure Google API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found in environment variables.")
genai.configure(api_key=GOOGLE_API_KEY)

# Model Configuration
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 1024
}

# Initialize Google Gemini model
gemini_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=MODEL_CONFIG
)


# Risk assessment processing
def process_risk_assessment(data):
    try:
        # Load the model and get feature importance
        model = load_xgboost_model(MODEL_PATH)
        feature_importance = get_feature_importance(model)
        formatted_importance = format_importance_for_prompt(feature_importance)

        # Create the prompt dynamically
        prompt = (
            f"You are an insurance risk assessment expert. Based on the following features and their relative importance, "
            f"provide a concise explanation of the calculated risk percentage ({data['riskPercentage']}%). "
            f"Focus on business insights to explain how each feature impacts the risk calculation, "
            f"emphasizing the most influential factors.\n\n"
            f"### Features and Importance:\n"
            f"{formatted_importance}\n\n"
            f"### Details for the specific case:\n"
            f"- **Age**: {data['age']}\n"
            f"- **Gender**: {data['gender']}\n"
            f"- **Vehicle Type**: {data['vehicleType']}\n"
            f"- **Total Claims**: {data['totalClaims']}\n"
            f"- **Reason for Claim**: {data['reason']}\n"
            f"- **Premium (LKR)**: {data['premium']}\n"
            f"- **Claim Amount (LKR)**: {data['claimAmount']}\n"
            f"- **Insured Period (Years)**: {data['insuredPeriod']}\n\n"
            f"Provide a concise business-focused analysis of how these factors contribute to the risk percentage."
            f"Avoid technical jargon and focus on actionable insights for the insurance company non technical staff.\n\n"
            f"Give recommendations for risk mitigation strategies based on premium and claim amount.\n\n"
            f"Use 5-6 sentences to summarize the key points.\n"
        )

        # Generate response from Google Gemini
        response = gemini_model.generate_content(prompt)
        return {"analysis": response.text} if response and response.text else {"error": "No response from model."}

    except Exception as e:
        logging.error(f"Error in risk assessment: {e}")
        return {"error": str(e)}