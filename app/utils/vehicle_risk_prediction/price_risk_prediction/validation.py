def validate_input(data):
    field_names = {
        "make": "Vehicle Make",
        "model": "Vehicle Model",
        "vehicle_type": "Vehicle Type",
        "year": "Manufacturing Year",
        "mileage": "Mileage (km)"
    }

    required_fields = field_names.keys()

    # Check for missing fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field_names[field]}."

    # Validate data types
    if not isinstance(data["make"], str) or not data["make"].strip():
        return False, f"Invalid '{field_names['make']}', must be a non-empty string."
    if not isinstance(data["model"], str) or not data["model"].strip():
        return False, f"Invalid '{field_names['model']}', must be a non-empty string."
    if not isinstance(data["vehicle_type"], str) or not data["vehicle_type"].strip():
        return False, f"Invalid '{field_names['vehicle_type']}', must be a non-empty string."

    try:
        data["year"] = int(data["year"])
        if data["year"] < 1990 or data["year"] > 2024:
            return False, f"Invalid '{field_names['year']}', must be between 1990 and 2024."
    except ValueError:
        return False, f"Invalid '{field_names['year']}', must be an integer."

    try:
        data["mileage"] = float(data["mileage"])
        if data["mileage"] < 0:
            return False, f"Invalid '{field_names['mileage']}', must be a positive number."
    except ValueError:
        return False, f"Invalid '{field_names['mileage']}', must be a number."

    return True, "Valid input."
