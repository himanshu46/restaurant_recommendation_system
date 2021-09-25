import pymongo
import pandas as pd
from geopy import Bing

def import_content(long,lat,min_cost=0, max_cost=100000,dist=20000):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['project']

    return (list(mng_db.restaurants.find({"$and": [{"coordinates": {
        "$geoNear": {"$geometry": {"type": 'Point', "coordinates": [long, lat]}, "$maxDistance": dist}}}, {"cost_for_two": {"$gte": min_cost, "$lte": max_cost}}]},{"_id": 0, "name": 1, "address": 1, "rate": 1, "cost_for_two": 1}).sort("score")))


def recommend_rest(add,min_cost=0, max_cost=100000,dist=20000):

    result = []

    api_key = "Asd_YyfsODTSJELwJ4F5feuHCiL1ORy-7MHuiuRR4uwTzZer00BMm4Vm2oWSjEHf"
    geolocator = Bing(api_key=api_key)
    coord = geolocator.geocode(add)
    lat = coord.latitude
    longit = coord.longitude

    ls = import_content(longit, lat, min_cost, max_cost, dist)
    if len(ls) == 0:
        return 0
    else:
        if len(ls)>=10:
            for i in range(-1,-10,-1):
                result.append(ls[i])
            return result
        else:
            for i in range(-1,-len(ls),-1):
                result.append(ls[i])
            return result