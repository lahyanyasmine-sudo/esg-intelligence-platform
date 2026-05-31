import joblib

model = joblib.load("../models/esg_model.pkl")
features = joblib.load("../models/features.pkl")
le_industry = joblib.load("../models/le_industry.pkl")
le_region = joblib.load("../models/le_region.pkl")