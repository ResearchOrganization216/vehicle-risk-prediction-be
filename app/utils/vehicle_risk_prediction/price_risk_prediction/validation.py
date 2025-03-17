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
        return False, f"Invalid '{field_names['make']}' or missing"
    if not isinstance(data["model"], str) or not data["model"].strip():
        return False, f"Invalid '{field_names['model']}'or missing"
    if not isinstance(data["vehicle_type"], str) or not data["vehicle_type"].strip():
        return False, f"Invalid '{field_names['vehicle_type']}' or missing"

    def is_valid_number(value, expected_type=int):
        """Check if a value is a valid number (int/float) even if it comes as a string."""
        try:
            return expected_type(value) if isinstance(value, (int, float, str)) and str(value).strip().isdigit() else None
        except ValueError:
            return None

    try:
        # Convert year to an integer safely
        year = is_valid_number(data["year"], int)
        if year is None or year < 1990 or year > 2024:
            return False, f"Invalid '{field_names['year']}', must be an year between 1990 and 2024."
        data["year"] = year  # Update the value after conversion
    except Exception:
        return False, f"Invalid '{field_names['year']}', must be an year."

    try:
        # Convert mileage to a float safely
        mileage = is_valid_number(data["mileage"], int)
        if mileage is None or mileage < 0:
            return False, f"Invalid '{field_names['mileage']}', must be a positive number."
        data["mileage"] = mileage  # Update the value after conversion
    except Exception:
        return False, f"Invalid '{field_names['mileage']}', must be a number."

    return True, "Valid input."
