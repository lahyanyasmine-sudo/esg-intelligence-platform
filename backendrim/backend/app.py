from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict_esg

app = FastAPI()

class ESGInput(BaseModel):
    Revenue: float
    ProfitMargin: float
    MarketCap: float
    GrowthRate: float
    CarbonEmissions: float
    WaterUsage: float
    EnergyConsumption: float
    Industry: str
    Region: str
    Year: float


@app.post("/predict")
def predict(data: ESGInput):
    return predict_esg(data.dict())