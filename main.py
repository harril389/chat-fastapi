import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sockets import sio_app
from database import get_collection, to_object_id

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def home():
    return {'message': 'Hello👋 Developers💻'}


@app.get('/example')
async def example():
    users_collection = get_collection("cat")
    print(users_collection)
    user = users_collection.find_one()
    return {"id": str(user["_id"]), "name": user["name"]}

app.mount('/', app=sio_app)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
