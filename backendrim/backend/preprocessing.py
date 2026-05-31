import pandas as pd
import numpy as np

def build_features(df):

    # features simples
    df["Profit_Growth"] = df["GrowthRate"] * df["ProfitMargin"]
    df["Size"] = np.log1p(df["MarketCap"])
    df["Efficiency"] = df["Revenue"] / (df["EnergyConsumption"] + 1)

    df["Year_norm"] = df["Year"] / 2025
    df["Revenue_growth_company"] = df["Revenue"] * df["GrowthRate"]

    # ESG proxy (IMPORTANT)
    df["ESG_Avg"] = (
        df["CarbonEmissions"] +
        df["WaterUsage"] +
        df["EnergyConsumption"]
    ) / 3

    df["ESG_Std"] = df[["CarbonEmissions","WaterUsage","EnergyConsumption"]].std(axis=1)

    return df