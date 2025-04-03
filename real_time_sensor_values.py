import pandas as pd


def get_sensor_data():
    df = pd.read_csv('sensor_data.csv')
    return {
        "heart_rate": df["heart_rate"].tolist(),
        "blood_pressure": df["blood_pressure"].tolist(),
        "temperature": df["temperature"].tolist()
    }


