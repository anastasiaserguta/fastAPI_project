from fastapi import FastAPI, Body, Form, Cookie, Header, HTTPException, Depends, status
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.requests import Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User, Feedback, UserCreate, UserAuth, USER_DATA, UserJwt, NEW_USERS
from random import randint
from typing import Annotated
from re import match
from datetime import datetime, timedelta, timezone
import jwt



test_app = FastAPI()
security = HTTPBasic()

SECRET_KEY = 'testsecretkey'
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="loginjwt")


@test_app.get('/')
async def root():
    # return {"message": "Hello World"} # JSON format
    return FileResponse('public/index.html')

@test_app.post('/')
def calculate(data=Body()):
    digit1 = data['digit1']
    digit2 = data['digit2']
    total = int(digit1) + int(digit2)
    return {'message': f'Сумма чисел {digit1} и {digit2} = {total}.'}

@test_app.get("/custom")
async def read_custom_message():
    return {"message": "This is a custom message!"}

# @test_app.get('/users')
# async def users() -> JSONResponse:
#     user = User(id=24, name='Anastasia Serguta')
#     return {'user': {'id': user.id, 'name': user.name}}

@test_app.get('/user')
async def root():
    return FileResponse('public/check_adult_user.html')

@test_app.post('/is_adult')
async def is_adult(data=Body()) -> JSONResponse:
    user = User(age=data['age'], name=data['name'])
    if int(data['age']) >= 18:
        is_adult = True
    else:
        is_adult = data['is_adult']
    return {'user': {'id': user.age, 'name': user.name, 'is_adult': is_adult}}

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
    3: {"username": "jane_not_smith", "email": "jane_not@example.com"},
    4: {"username": "smith", "email": "smith@example.com"},
    5: {"username": "jane_xexe", "email": "jane_xexe@example.com"},
}

@test_app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}

@test_app.get("/users/")
def read_users(limit: int = 4):
    return dict(list(fake_users.items())[:limit])

@test_app.get('/feedback')
async def get_feedback():
    return FileResponse('public/feedback.html')

@test_app.post('/feedback')
async def feedback(data=Body()) -> JSONResponse:
    user_feedback = Feedback(name=data['name'], message=data['feedback'])
    return {"message": f"Feedback received. Thank you, {user_feedback.name}"}

test_simple_db = []

@test_app.post('/create_user')
async def create_user(new_user: UserCreate) -> UserCreate: 
    test_simple_db.append(new_user)
    return new_user

@test_app.get('/show_users')
async def show_users() -> JSONResponse:
    return {'all_users': test_simple_db}

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}
sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}
sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}
sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}
sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


@test_app.get('/product/{product_id}')
async def product(product_id: int) -> JSONResponse:
    for pr in sample_products:
        if pr['product_id'] == product_id:
            return {'product': pr}
        
    return {'product': 'not found'}
    
@test_app.get('/products/search/')
async def search(keyword: str, category: str | None = None, limit: int | None = 10) -> JSONResponse:
    total = []
    if category is not None:
        for pr in sample_products:
            if keyword.lower() in pr['name'].lower() and pr['category'] == category:
                total.append(pr)
    else:
        for pr in sample_products:
            if keyword.lower() in pr['name'].lower():
                total.append(pr)
    if len(total) == 0:
        return {'product': 'not found'}
    else:
        if limit is None:
            return {f'product in category {category}': total}
        else:
            return {f'product in category {category}': total[:limit]}

@test_app.get('/login')
async def root():
    return FileResponse('public/login.html')

fake_db_with_passwords = {
    'nastia': ['123', None],
    'lena': ['123', None],
    'fiona': ['1234', None],
}


@test_app.post('/logged')
async def logged(response: Response, username=Form(), password=Form()):
    global token
    if username in fake_db_with_passwords.keys():
        if fake_db_with_passwords[username][0] == password:
            token = ''.join([str(randint(0, 55)) for _ in range(20)])
            response.set_cookie(key='session_token', value=token, httponly=True)
            fake_db_with_passwords[username][1] = token
            return {'name': username, 'password': password, 'code': fake_db_with_passwords[username][1]}
        else:
            return{username: 'incorrect password'}
    else:
        return {'error': 'user not found'}

@test_app.get('/user_profile')
async def user_profile(session_token = Cookie()):
    for user in fake_db_with_passwords.keys():
        if session_token == fake_db_with_passwords[user][1]:
            return {'username': user, 'password':fake_db_with_passwords[user][0]}
    return {'message': 'Unauthorized'}

@test_app.get('/headers')
async def read_data(user_agent: Annotated[str | None, Header()] = None, accept_language: Annotated[str | None, Header()] = None):
    reg_pattern = r'(^[a-z]{2}\-[A-Z]{2},[a-z]{2};?)(q=[0-9.]{3}?)'
    if user_agent is None or accept_language is None or not match(reg_pattern, accept_language):
        raise HTTPException(400)
    else:
        return {
            'User-agent': user_agent,
            'Accept-Language': accept_language,
        }

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    return user

def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

@test_app.get("/succesauth/")
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {"secret message": "You got my secret, welcome!", "user_info": user}

NEW_USERS = {
    "admin": {"username": "admin", "password": "adminpass", "role": "admin"},
    "user": {"username": "user", "password": "userpass", "role": "user"},
}

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        exp_time = payload.get('exp')
        username = payload.get('sub') 
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user(username: str):
    if username in NEW_USERS:
        user_data = NEW_USERS[username]
        return UserJwt(**user_data)
    return None

@test_app.post('/loginjwt')
async def loginjwt(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_data_from_db = get_user(data.username)
    if user_data_from_db is None or data.password != user_data_from_db.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_jwt_token({'sub': data.username, 'exp': datetime.now(timezone.utc) + timedelta(minutes=3)})}
    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@test_app.get('/protected_resource/')
async def protected_resourse(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": "Auth succes!", "token_data": payload}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
@test_app.get("/admin/")
def get_admin_info(current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"message": "Welcome admin!"}

@test_app.get("/user/")
def get_user_info(current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"message": "Hello User!"}