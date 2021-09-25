import joblib
import pandas as pd
import numpy as np
import geopy as gp
from geopy import Bing

def recommend_rest(add):
    api_key = "Asd_YyfsODTSJELwJ4F5feuHCiL1ORy-7MHuiuRR4uwTzZer00BMm4Vm2oWSjEHf"
    geolocator = Bing(api_key=api_key)
    coord = geolocator.geocode(add)
    lat = coord.latitude
    longit = coord.longitude
    model = joblib.load("filename.pkl")
    predict = model.predict([[lat,longit]])

    # print(predict)
    df  = pd.read_csv("final1.csv")
    df1 = df[df["cluster"]==predict[0]]
    df1.head()
    df2 = df1.sort_values(by=["score"],ascending=False).iloc[:10]
    df3= df2[["name", "address", "rate", "votes", "cost_for_two"]]
    return df3

