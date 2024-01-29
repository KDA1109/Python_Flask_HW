from typing import List
import databases
import pandas as pd
import sqlalchemy
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates


DATABASE_URL = "sqlite:///store.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("surname", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="./Homeworks/Final/templates")

class User(BaseModel):
    username: str = Field(..., max_length=40, min_length=2)
    surname: str = Field(..., max_length=40, min_length=2)
    email: str = Field(..., max_length=120)
    password: str = Field(..., min_length=5)

class Order(BaseModel):
    user_id: int
    product_id: int
    order_date: str = Field(..., max_length=40)
    status: str = Field(..., max_length=40)

class Product(BaseModel):
    name: str = Field(..., max_length=40)
    description: str = Field(max_length=250)
    price: float = Field(gt=0)


@app.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    query = users.select()
    user_table = pd.DataFrame([user for user in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse("users.html", {"request": request, "user_table": user_table})

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

@app.post("/users", response_model=User)
async def create_user(user: User):
    query = users.insert().values(**user.model_dump())
    record_id = await database.execute(query)
    return {**user.dict(), "id": record_id}

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: User):
    query = (users.update().where(users.c.id == user_id).values(**new_user.model_dump()))
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}

@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted!"}

@app.get("/products", response_class=HTMLResponse)
async def read_products(request: Request):
    query = products.select()
    product_table = pd.DataFrame([product for product in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse("products.html", {"request": request, "product_table": product_table})

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)

@app.post("/products", response_model=Product)
async def create_product(product: Product):
    query = products.insert().values(**product.model_dump())
    record_id = await database.execute(query)
    return {**product.dict(), "id": record_id}

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: Product):
    query = (products.update().where(products.c.id == product_id).values(**new_product.model_dump()))
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}

@app.delete("/products/delete/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Product deleted!"}

@app.get("/orders", response_class=HTMLResponse)
async def read_orders(request: Request):
    query = orders.select()
    order_table = pd.DataFrame([order for order in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse("orders.html", {"request": request, "order_table": order_table})

@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)

@app.post("/orders", response_model=Order)
async def create_order(order: Order):
    query = orders.insert().values(**order.model_dump())
    record_id = await database.execute(query)
    return {**order.model_dump(), "id": record_id}

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: Order):
    query = (orders.update().where(orders.c.id == order_id).values(**new_order.model_dump()))
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}

@app.delete("/orders/delete/{order_id}")
async def delete_product(order_id: int):
    query = products.delete().where(products.c.id == order_id)
    await database.execute(query)
    return {"message": "Order deleted!"}


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()