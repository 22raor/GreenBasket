from fastapi import FastAPI

import pymongo
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

    listOfAlternatives = api.product.getAlternatives(deepestCategory).json()["products"]

    listOfAlternatives.sort(key= lambda x: x['ecoscore_score'], reverse=True)

    imageURL = prod["product"]["image_url"]

    

    ret = {"name": name, "score": ecoscore, "alts": listOfAlternatives, "image": imageURL}

    return {"res": ret}


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