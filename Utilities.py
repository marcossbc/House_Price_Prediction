import pandas as pd
import joblib, json

# Load once at import
CURRENT_YEAR = 2025
TRAIN_COLUMNS = json.load(open("modeles/train_columns.json"))
SCALER = joblib.load("modeles/house_scaler.pkl")

# feutures engineering, one-hot, scalling
def prepare_features_from_raw(record: dict) -> pd.DataFrame:
  
  size = float(record.get("Size_m2", 0.0))
  beds = int(record.get("Bedrooms", 0.0))
  baths = int(record.get("Bathrooms", 0.0))
  year = int(record.get("YearBuilt", CURRENT_YEAR))
  loc = str(record.get("Location", "city"))

  house_age = CURRENT_YEAR - year
  Rooms_per_1000m2 = ((beds + baths) / (size / 1000)) if size else 0.0
  Size_per_Bedroom = (size / beds) if beds else 0.0
  is_city = 1 if loc.lower() == "city" else 0

  row = {col: 0.0 for col in TRAIN_COLUMNS}
  for name, val in [
    ("Size_m2", size),
    ("Bedrooms", beds),
    ("Bathrooms", baths),
    ("YearBuilt", year),
    ("HouseAge", house_age),
    ("Rooms_per_1000m2", Rooms_per_1000m2),
    ("Size_per_Bedroom", Size_per_Bedroom),
  ]:
    if name in row:
      row[name] = float(val)
      
      
  # One-hot for Location
  loc_col = f"Location_{loc}"    #loc waa city, Suburb
  if loc_col in row:
    row[loc_col] = 1.0

  df_one = pd.DataFrame([row], columns=TRAIN_COLUMNS)

  # Scale only the columns the scaler was fitted on
  if hasattr(SCALER, "feature_names_in_"):
    cols_to_scale = list(SCALER.feature_names_in_)
    df_one[cols_to_scale] = SCALER.transform(df_one[cols_to_scale])


  return df_one  

