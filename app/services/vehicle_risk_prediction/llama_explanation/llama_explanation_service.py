import logging
from app.utils.vehicle_risk_prediction.llama_explanation.risk_assesment_utils_llama import get_groq_client

# Initialize the LLaMA client
client = get_groq_client()

# Configure logging
logger = logging.getLogger(__name__)

# Dummy previous data (since the database is not connected)
previous_premium = 10000 
previous_risk_score = 85 

def calculate_total_risk_score(risk_data):
    weights = {
        "predicted_claim_risk_rank": 0.5,
        "predicted_market_risk_score": 0.4,
        "predicted_spare_parts_risk_percentage": 0.1
    }

    # Normalize the values (you can adjust this based on your actual data)
    normalized_claim_risk_rank = risk_data.get("predicted_claim_risk_rank", 0) 
    normalized_market_risk_score = risk_data.get("predicted_market_risk_score", 0) 
    normalized_spare_parts_risk_percentage = risk_data.get("predicted_spare_parts_risk_percentage", 0) 

    # Calculate total risk score as the weighted sum of all normalized values
    total_risk_score = (
        normalized_claim_risk_rank * weights["predicted_claim_risk_rank"] +
        normalized_market_risk_score * weights["predicted_market_risk_score"] +
        normalized_spare_parts_risk_percentage * weights["predicted_spare_parts_risk_percentage"]
    )

    # Return the total risk score
    return round(total_risk_score, 2)

def calculate_premium_adjustment(current_risk_score):
    risk_score_change_percentage = ((current_risk_score - previous_risk_score) / previous_risk_score) * 100

    logger.info(f"Risk score change: {risk_score_change_percentage}%")

    # Define the premium adjustment logic
    if risk_score_change_percentage <= 5:
        # Low Risk: Apply a discount (10% reduction)
        adjusted_premium = previous_premium * 0.90
        adjustment_factor = "Discount (10%)"
    elif 5 < risk_score_change_percentage <= 7:
        # Moderate Risk: Keep premium the same
        adjusted_premium = previous_premium
        adjustment_factor = "No Change"
    elif 7 < risk_score_change_percentage <= 10:
        # High Risk: Increase the premium significantly (+20%)
        adjusted_premium = previous_premium * 1.20
        adjustment_factor = "Increase (20%)"
    else:
        # Extreme change (beyond 10%): Handle as a special case
        adjusted_premium = previous_premium * 1.30 
        adjustment_factor = "Extreme Increase (30%)"

    return adjusted_premium, adjustment_factor

def generate_lama_explanation(risk_data):

    risk_score_change_percentage = ((calculate_total_risk_score(risk_data) - previous_risk_score) / previous_risk_score) * 100
    try:
        # Build the prompt for LLaMA based on risk score change percentage
        if risk_score_change_percentage <= 5:
            prompt = (
                "Act as an Insurance premium specialist. Please explain why a discount is being applied to the premium, "
                "in a way that the vehicle owner (policyholder) can easily understand. "
                "Discuss how changes in the market, total claims, and spare parts availability have contributed to the lower risk score, "
                "leading to a reduction in the premium. Keep the response to three sentences, simple, clear, and professional for the user. "
                "Also, advise the policyholder on any actions they can take to further benefit from the premium reduction."
            )
        elif 5 < risk_score_change_percentage <= 7:
            prompt = (
                "Act as an Insurance premium specialist. Please explain why the premium is not changing, "
                "in a way that the vehicle owner (policyholder) can easily understand. "
                "Discuss how the market, claims, and spare parts availability have remained stable, causing no significant change in the risk score or the premium. "
                "Keep the response to three sentences, simple, clear, and professional for the user. "
                "Additionally, provide guidance on what the policyholder can do to maintain this stable premium moving forward."
            )
        elif 7 < risk_score_change_percentage <= 10:
            prompt = (
                "Act as an Insurance premium specialist. Please explain why the premium is increasing significantly, "
                "in a way that the vehicle owner (policyholder) can easily understand. "
                "Discuss the factors driving the increased risk score, such as higher market values, more claims, or issues with spare parts availability, "
                "and how these are contributing to the premium increase. Keep the response to three sentences, simple, clear, and professional for the user. "
                "Then, suggest what steps the policyholder can take to manage or possibly lower their premium in the future. "
                "Also, inform the policyholder that if they do not accept the premium increase, they may receive a lower claim payout when they file a claim."
            )
        else:
            prompt = (
                "Act as an Insurance premium specialist. Please provide an explanation for the extreme change in premium, "
                "in a way that the vehicle owner (policyholder) can easily understand. "
                "Explain how significant changes in market value, claims, or spare parts availability have dramatically increased the risk score, "
                "leading to a large increase in the premium. Keep the response to three sentences, simple, clear, and professional for the user. "
                "Finally, advise the policyholder on actions they can take to mitigate this dramatic premium increase in the future. "
                "Also, let them know that rejecting the premium increase may result in lower claim amounts when they need to make a claim."
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
            model="llama-3.3-70b-versatile"
        )

        # Extract the response content
        explanation = analysis.choices[0].message.content.strip()
        logger.info(f"LLaMA explanation generated: {explanation}")

        # Calculate the total risk score
        total_risk_score = calculate_total_risk_score(risk_data)
        logger.info(f"Calculated Total Risk Score: {total_risk_score}")

        # Calculate premium adjustment
        adjusted_premium, adjustment_factor = calculate_premium_adjustment(total_risk_score)

        # Return the explanation, total risk score, and adjusted premium in the response
        return explanation, total_risk_score, adjusted_premium, adjustment_factor

    except Exception as e:
        logger.error(f"Error generating LLaMA explanation: {str(e)}", exc_info=True)
        raise Exception("Failed to generate insurance explanation")
