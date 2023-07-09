from fastapi import FastAPI, HTTPException
import pymongo as py
from bson import ObjectId
from datetime import datetime
from typing import List
from pydantic import BaseModel


app = FastAPI()

# Connect to MongoDB
client =py.MongoClient("mongodb://localhost:27017")
db = client["ecommerce"]
products_collection = db["products"]
orders_collection = db["orders"]




@app.get("/products")
def get_products():
    products = list(products_collection.find())
    serialized_products = []
    for product in products:
        serialized_product = {
            "_id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "quantity": product["quantity"]
        }
        serialized_products.append(serialized_product)
    return {"products": serialized_products}


class Item(BaseModel):
    productId: str
    boughtQuantity: int

class UserAddress(BaseModel):
    City: str
    Country: str
    ZipCode: str

class Order(BaseModel):
    timestamp: datetime
    items: List[Item]
    totalAmount: float
    userAddress: UserAddress

@app.post("/orders")
def create_order(order: Order):
    # Connect to MongoDB
    client = py.MongoClient("mongodb://localhost:27017")
    db = client["ecommerce"]
    orders_collection = db["orders"]

    # Convert the order object to a dictionary
    order_dict = order.dict()

    # Insert the order into the MongoDB collection
    inserted_order = orders_collection.insert_one(order_dict)

    return {
        "message": "Order created successfully",
        "order_id": str(inserted_order.inserted_id)
    }


class Order(BaseModel):
    order_id: str
    timestamp: str
    items: List[str]
    total_amount: float
    user_address: dict

@app.get("/orders")
def get_orders(limit: int = 10, offset: int = 0):
    # Connect to MongoDB
    client = py.MongoClient("mongodb://localhost:27017")
    db = client["ecommerce"]
    orders_collection = db["orders"]

    # Fetch orders with pagination
    orders = list(orders_collection.find().skip(offset).limit(limit))

    # Transform orders to Order objects
    transformed_orders = []
    for order in orders:
        transformed_order = Order(
            order_id=str(order["_id"]),
            timestamp=str(order["timestamp"]),
            items=[item["productId"] for item in order["items"]],
            total_amount=order["totalAmount"],
            user_address=order["userAddress"]
        )
        transformed_orders.append(transformed_order)

    return transformed_orders

class Order(BaseModel):
    order_id: str
    timestamp: str
    items: list
    total_amount: float
    user_address: dict

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    # Connect to MongoDB
    client = py.MongoClient("mongodb://localhost:27017")
    db = client["ecommerce"]
    orders_collection = db["orders"]

    # Fetch the order by ID
    order = orders_collection.find_one({"_id": order_id})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Transform the order to an Order object
    transformed_order = Order(
        order_id=str(order["_id"]),
        timestamp=str(order["timestamp"]),
        items=order["items"],
        total_amount=order["totalAmount"],
        user_address=order["userAddress"]
    )

    return transformed_order

class Product(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

@app.put("/products/{product_id}")
def update_product(product_id: str, quantity: int):
    # Connect to MongoDB
    client = py.MongoClient("mongodb://localhost:27017")
    db = client["ecommerce"]
    products_collection = db["products"]

    # Find the product by ID
    product = products_collection.find_one({"_id": product_id})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product's quantity
    products_collection.update_one(
        {"_id": product_id},
        {"$set": {"quantity": quantity}}
    )

    # Return the updated product
    updated_product = Product(
        product_id=str(product["_id"]),
        name=product["name"],
        price=product["price"],
        quantity=quantity
    )

    return updated_product

