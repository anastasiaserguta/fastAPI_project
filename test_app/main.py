from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, JSONResponse
from models import User, Feedback


test_app = FastAPI()


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






