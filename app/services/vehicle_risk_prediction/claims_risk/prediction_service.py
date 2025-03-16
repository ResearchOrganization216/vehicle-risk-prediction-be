import pandas as pd
import os
from rapidfuzz import process, fuzz
from app.config import logger
import random 

# Load the CSV file
csv_path = os.path.join('app', 'models', 'vehicle_risk_prediction', 'ranked_insurance_claims.csv')
insurance_claims_df = pd.read_csv(csv_path)

# Preprocessing function
def preprocess_text_field(value):
    return pd.Series(value).str.lower().str.replace(r'[^\w]', '', regex=True).iloc[0]

def calculate_insurance_risk(make, model):
    """Returns the risk rank for a given make and model using fuzzy matching."""
    try:
        # Preprocess input values
        make = preprocess_text_field(make)
        model = preprocess_text_field(model)

        # Preprocess dataset
        insurance_claims_df["Make"] = insurance_claims_df["Make"].apply(preprocess_text_field)
        insurance_claims_df["Model"] = insurance_claims_df["Model"].apply(preprocess_text_field)

        # Filter dataset by Make (Exact Match)
        make_filtered_df = insurance_claims_df[insurance_claims_df["Make"] == make]

        if make_filtered_df.empty:
            logger.warning(f"No records found for make: {make}")
            rank = round(random.uniform(70, 80), 2)  # Assign random rank
            return {
                "risk_rank": int(rank)
            }

        # Fuzzy match for Model
        model_choices = make_filtered_df["Model"].unique()
        match_result = process.extractOne(model, model_choices, scorer=fuzz.partial_ratio, score_cutoff=60)

        if match_result:
            if len(match_result) == 2:
                best_match, score = match_result  # Handle older versions
            else:
                best_match, score, *_ = match_result  # Handle newer versions
        else:
            best_match = None

        if best_match:
            matched_row = make_filtered_df[make_filtered_df["Model"] == best_match]
        else:
            matched_row = pd.DataFrame() 

        if not matched_row.empty:
            # Check if 'rank' column exists
            if 'rank' in matched_row.columns:
                rank = matched_row.iloc[0]["rank"]
            else:
                logger.warning(f"'rank' column missing for model: {best_match}")
                rank = round(random.uniform(60, 80), 2)  # Assign random rank
                return {
                    "risk_rank": int(rank)
                } 
        else:
            logger.warning(f"No close model match found for: {model}")
            rank = round(random.uniform(70, 80), 2)  
            return {
                "risk_rank": int(rank)
            }

        if rank >= 90:
            rank = round(random.uniform(80, 90), 2)

        return {
            "risk_rank": int(rank)
        }

    except Exception as e:
        logger.error(f"Error fetching insurance risk rank: {str(e)}", exc_info=True)
        return None
