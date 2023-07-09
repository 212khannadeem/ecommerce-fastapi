# ecommerce-fastapi
FastAPI Ecommerce Application
============================

This is a simple ecommerce application built using FastAPI and Python. It provides a set of APIs to manage products and orders.

Features
--------

- List all available products
- Create a new order
- Fetch all orders with pagination
- Fetch a single order by ID
- Update the available quantity for a product

Installation
------------

1. Clone the repository:

   git clone <repository_url>

2. Install the required dependencies:

   pip install -r requirements.txt

Usage
-----

1. Start the FastAPI server:

   uvicorn main:app --reload

2. Access the APIs using the provided URLs:

   - List all available products:
     - GET /products

   - Create a new order:
     - POST /orders

   - Fetch all orders with pagination:
     - GET /orders?limit=<limit>&offset=<offset>

   - Fetch a single order by ID:
     - GET /orders/<order_id>

   - Update the available quantity for a product:
     - PUT /products/<product_id>?quantity=<quantity>

3. Test the APIs using tools like Postman or cURL.

Sample Requests and Responses
-----------------------------

- Create a new order:
  - Request:
    POST /orders
    {
      "items": [
        {
          "productId": 1,
          "boughtQuantity": 2
        },
        {
          "productId": 2,
          "boughtQuantity": 1
        }
      ]
    }
  - Response:
    {
      "orderId": 1,
      "items": [
        {
          "productId": 1,
          "boughtQuantity": 2
        },
        {
          "productId": 2,
          "boughtQuantity": 1
        }
      ],
      "totalAmount": 2000.0
    }

- Fetch all orders with pagination:
  - Request:
    GET /orders?limit=10&offset=0
  - Response:
    [
      {
        "orderId": 1,
        "items": [
          {
            "productId": 1,
            "boughtQuantity": 2
          },
          {
            "productId": 2,
            "boughtQuantity": 1
          }
        ],
        "totalAmount": 2000.0
      }
    ]

- Fetch a single order by ID:
  - Request:
    GET /orders/1
  - Response:
    {
      "orderId": 1,
      "items": [
        {
          "productId": 1,
          "boughtQuantity": 2
        },
        {
          "productId": 2,
          "boughtQuantity": 1
        }
      ],
      "totalAmount": 2000.0
    }

- Update the available quantity for a product:
  - Request:
    PUT /products/1?quantity=5
  - Response:
    {
      "id": 1,
      "name": "TV",
      "price": 500,
      "quantity": 5
    }

