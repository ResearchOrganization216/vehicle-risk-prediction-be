def validate_insurance_risk_input(data):
    """Validates user input for insurance risk calculation."""
    required_fields = ["make", "model"]
    
    # Check if required fields are present
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field.capitalize()} is required"

    return True, "Valid input"
