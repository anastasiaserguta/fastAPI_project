from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, JSONResponse
from models import User, Feedback, UserCreate


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

