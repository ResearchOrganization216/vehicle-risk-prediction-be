def validate_spare_parts_risk_input(data):
    field_names = {
        "make": "Vehicle Make",
        "model": "Vehicle Model",
        "vehicle_type": "Vehicle Type",
        "year": "Manufacturing Year"
    }

    required_fields = field_names.keys()

    # Check for missing fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field_names[field]}."

    # Validate data types for strings
    for field in ["make", "model", "vehicle_type"]:
        if not isinstance(data[field], str) or not data[field].strip():
            return False, f"Invalid '{field_names[field]}', must be a non-empty string."

    # Validate year
    try:
        data["year"] = int(data["year"])
        if data["year"] < 1990 or data["year"] > 2024:
            return False, f"Invalid '{field_names['year']}', must be between 1990 and 2024."
    except ValueError:
        return False, f"Invalid '{field_names['year']}', must be an integer."

    return True, "Valid input."
