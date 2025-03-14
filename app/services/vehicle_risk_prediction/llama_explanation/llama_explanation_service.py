import logging
from app.utils.vehicle_risk_prediction.llama_explanation.risk_assesment_utils_llama import get_groq_client

# Initialize the LLaMA client
client = get_groq_client()

# Configure logging
logger = logging.getLogger(__name__)

def generate_lama_explanation(risk_data):
    try:
        # Build the prompt for LLaMA
        prompt = (
            f"You are an expert in vehicle insurance risk assessment. Based on the following risk factors, "
            f"provide a detailed explanation of how they impact the insurance premium:\n\n"
            f"- **Insurance Claim Risk Rank**: {risk_data.get('predicted_claim_risk_rank', 'N/A')}\n"
            f"- **Market Risk Score**: {risk_data.get('predicted_market_risk_score', 'N/A')}\n"
            f"- **Predicted Vehicle Price**: {risk_data.get('predicted_price', 'N/A')}\n"
            f"- **Spare Parts Risk Percentage**: {risk_data.get('predicted_spare_parts_risk_percentage', 'N/A')}\n\n"
            f"Analyze these risk scores and explain their impact on the insurance premium. "
            f"Provide insights relevant to the Sri Lankan vehicle insurance industry, considering local market trends, "
            f"claim behaviors, and risk management strategies. Keep the response concise (5-6 sentences) and practical "
            f"for insurance professionals."
        )

        # Generate explanation using LLaMA
        analysis = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a Specialist in the Vehicle Insurance industry"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model="llama-3.3-70b-versatile"  # Adjust based on your LLaMA model
        )

        # Extract the response content
        explanation = analysis.choices[0].message.content.strip()
        logger.info(f"LLaMA explanation generated: {explanation}")

        return explanation

    except Exception as e:
        logger.error(f"Error generating LLaMA explanation: {str(e)}", exc_info=True)
        raise Exception("Failed to generate insurance explanation")
