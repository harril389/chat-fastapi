from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sockets import sio_app
from database import get_collection

from security import generate_token, pwd_context, verify_password

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/example')
async def example():
    users_collection = get_collection("cat")
    print(users_collection)
    user = users_collection.find_one()
    return {"id": str(user["_id"]), "name": user["name"]}


class User(BaseModel):
    username: str
    password: str


@app.post('/register')
async def register(user: User):
    users_collection = get_collection('user')
    existing_user = users_collection.find_one({'username': user.username})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Tài khoản người dùng đã tồn tại")
    hashed_password = pwd_context.hash(user.password)
    users_collection.insert_one(
        {'username': user.username, 'password': hashed_password})
    return {"message": "Đăng ký tài khoản người dùng thành công"}


@app.post('/login')
async def login(user: User):
    users_collection = get_collection('user')
    existing_user = users_collection.find_one({'username': user.username})
    if not existing_user:
        raise HTTPException(status_code=404, detail='Tài khoản không tồn tại')
    check_password = verify_password(existing_user, user.password)
    if not check_password:
        raise HTTPException(status_code=404, detail='Sai mật khẩu')
    token = generate_token(existing_user["username"])
    return {'token': token}

app.mount('/', app=sio_app)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
