from model_loader import model, features, le_industry, le_region
from preprocessing import build_features
import pandas as pd

def predict_esg(data: dict):

    df = pd.DataFrame([data])

    # encodage
    df["Industry_enc"] = le_industry.transform([data["Industry"]])[0]
    df["Region_enc"] = le_region.transform([data["Region"]])[0]

    # build engineered features
    df = build_features(df)

    # align features EXACT TRAINING
    X = df.reindex(columns=features, fill_value=0)

    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.fillna(0)

    pred = model.predict(X)[0]

    labels = {
        0: "Très faible",
        1: "Faible",
        2: "Moyen",
        3: "Bon",
        4: "Excellent"
    }

    return {
        "prediction": int(pred),
        "label": labels[int(pred)]
    }