from fastapi import FastAPI

import pymongo
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://epic:epic@greenbasketdb.ilubdxm.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

from openfoodfacts import API, APIVersion, Country, Environment, Flavor

api = API(
    username="22raor",
    password="tgn1ZRH9vdc.dbg2bph",
    country=Country.us,
    flavor=Flavor.off,
    version=APIVersion.v2,
    environment=Environment.org,
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/eco_score/{id}")
async def root(id):
    return {"eco_score": int(id) // 2}

@app.get("/autocomplete/{product_query}")
async def autocomplete(product_query: str):
    return searchEngine(product_query)

@app.get("/productPage/{id}")
async def product(id: str):
    return giveProdGetInfo(id)
            



def giveProdGetInfo(id: str):
    prod = api.product.get(id)
    name = prod["product"]["product_name"]

    ecoscore = prod["product"]["ecoscore_score"]

    categories = prod["product"]["categories_hierarchy"]
    deepestCategory = categories[len(categories)-1]

    listOfAlternatives = getAlternatives(deepestCategory).json()["products"]

    listOfAlternatives.sort(key= lambda x: x['ecoscore_score'], reverse=True)

    imageURL = prod["product"]["image_url"]


    co2_agriculture = prod["product"]["ecoscore_data"]["agribalyse"]["co2_agriculture"]
    co2_consumption = prod["product"]["ecoscore_data"]["agribalyse"]["co2_consumption"]
    co2_distribution = prod["product"]["ecoscore_data"]["agribalyse"]["co2_distribution"]
    co2_packaging = prod["product"]["ecoscore_data"]["agribalyse"]["co2_packaging"]
    co2_processing = prod["product"]["ecoscore_data"]["agribalyse"]["co2_processing"]
    co2_total = prod["product"]["ecoscore_data"]["agribalyse"]["co2_total"]
    co2_transportation = prod["product"]["ecoscore_data"]["agribalyse"]["co2_transportation"]
    ef_agriculture = prod["product"]["ecoscore_data"]["agribalyse"]["ef_agriculture"]
    ef_consumption = prod["product"]["ecoscore_data"]["agribalyse"]["ef_consumption"]
    ef_distribution = prod["product"]["ecoscore_data"]["agribalyse"]["ef_distribution"]
    ef_packaging = prod["product"]["ecoscore_data"]["agribalyse"]["ef_packaging"]
    ef_processing = prod["product"]["ecoscore_data"]["agribalyse"]["ef_processing"]
    ef_total = prod["product"]["ecoscore_data"]["agribalyse"]["ef_total"]
    ef_transportation = prod["product"]["ecoscore_data"]["agribalyse"]["ef_transportation"]

    ret = {"name": name, "score": ecoscore, "alts": listOfAlternatives, "image": imageURL, "co2_agriculture": co2_agriculture, "co2_consumption": co2_consumption,
           "co2_distribution": co2_distribution, "co2_packaging": co2_packaging, "co2_processing": co2_processing, "co2_total": co2_total, "co2_transportation": co2_transportation,
           "ef_agriculture": ef_agriculture, "ef_consumption": ef_consumption, "ef_distribution": ef_distribution, "ef_packaging": ef_packaging, "ef_processing": ef_processing,
           "ef_total": ef_total, "ef_transportation": ef_transportation}

    return {"res": ret}

def getAlternatives(category):
        headers = { 
            'accept': 'application/json',
            'User-Agent': 'greenbasket/1.0'
        }
        params = {
            'categories_tags': category,
            'fields': 'code,product_name,ecoscore_score',
        }

        response = requests.get('https://us.openfoodfacts.org/api/v2/search', params=params, headers=headers)

        return response


def searchEngine(toSearch):
    # define pipeline
    pipeline = [
        {
            '$search': {
                'index': 'name_search', 
                'autocomplete': {
                    'query': toSearch, 
                    'path': 'product_name'
                }
            }
        }, {
            '$limit': 5
        }
    ]
    # run pipeline
    result = client["products"]["foodfacts"].aggregate(pipeline)

    res = []
    for i in result:
        i.pop("_id")
        res.append(i)
    return {"result":res}