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
            return False, f"Invalid '{field_names['year']}', must be an integer between 1990 and 2024."
        data["year"] = year  # Update the value after conversion
    except Exception:
        return False, f"Invalid '{field_names['year']}', must be an integer."

    return True, "Valid input."
