from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

# Создаем объект FastAPI
app = FastAPI()

# Настроим Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Инициализируем пустой список пользователей
users: List['User'] = []

# Модель User, которая будет хранить информацию о пользователе
class User(BaseModel):
    id: int
    username: str
    age: int

# GET запрос для отображения списка всех пользователей
@app.get("/", response_class=Jinja2Templates)
def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# GET запрос для отображения конкретного пользователя по ID
@app.get("/user/{user_id}", response_class=Jinja2Templates)
def get_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user:
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User not found")

# POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}", response_model=User)
def add_user(username: str, age: int):
    # Находим новый id для пользователя
    user_id = users[-1].id + 1 if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# PUT запрос для обновления данных пользователя
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
def update_user(user_id: int, username: str, age: int):
    # Ищем пользователя по user_id
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    
    # Если пользователь не найден, выбрасываем ошибку 404
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}", response_model=User)
def delete_user(user_id: int):
    # Ищем пользователя по user_id
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    
    # Если пользователь не найден, выбрасываем ошибку 404
    raise HTTPException(status_code=404, detail="User was not found")


@app.on_event("startup")
def create_users():
    # Создание нескольких пользователей
    add_user("UrbanUser", 24)
    add_user("UrbanTest", 22)
    add_user("Capybara", 60)
