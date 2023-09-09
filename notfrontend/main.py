from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/eco_score/{id}")
async def root(id):
    return {"eco_score": id // 2}