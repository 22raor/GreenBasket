from fastapi import FastAPI

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://epic:epic@greenbasketdb.ilubdxm.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/eco_score/{id}")
async def root(id):
    return {"eco_score": int(id) // 2}

@app.get("/autocomplete/{product_query}")
async def autocomplete(product_query: str):
    return {searchEngine(product_query)}


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

    return result