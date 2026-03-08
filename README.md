Tech Dukaan – Scalable E-commerce Backend API built with FastAPI

Tech Dukaan is a RESTful E-commerce Backend API built using FastAPI, PostgreSQL, SQLite and SQLAlchemy.
The project implements authentication, role-based access control, product management, cart system, and order processing.

--------------------------------------------------

Tech Stack

FastAPI
SQLAlchemy
SQLite (default for local development)
PostgreSQL (production ready)
JWT Authentication
Pydantic
Uvicorn

--------------------------------------------------

Key Features

JWT Authentication
Role Based Access Control (User / Seller)
Product CRUD APIs
Advanced Product Filtering
Pagination
Cart Management
Order Management
Product Data Ingestion Pipeline
Relational Database Models

--------------------------------------------------

Project Structure

app/
 ├── models        → SQLAlchemy database models
 ├── routes        → API endpoints
 ├── services      → Business logic layer
 ├── dependencies  → Authentication & DB dependencies
 ├── utils         → Helper functions
 ├── data          → Product dataset (JSON)
 ├── database.py   → Database connection
 └── main.py       → FastAPI application entry point

--------------------------------------------------

Authentication System

JWT based authentication is implemented.

APIs:

POST /auth/register  
POST /auth/login  

--------------------------------------------------

Seller System

Users can convert their account to a seller.

POST /seller/become-seller

Only sellers can:

create products  
update products  
delete products  

--------------------------------------------------

Product Management APIs

GET /products  
GET /products/{product_id}  
POST /products  
PUT /products/{product_id}  
DELETE /products/{product_id}  

--------------------------------------------------

Product Filtering and Search

Examples:

/products?page=1&limit=10  
/products?min_price=10000  
/products?max_price=50000  
/products?brand=samsung  
/products?search=iphone  
/products?sort_by=price&order=desc  

--------------------------------------------------

Cart System

POST /cart  
GET /cart  
DELETE /cart/{cart_item_id}  

--------------------------------------------------

Order System

POST /orders  
GET /orders  
DELETE /orders/{order_id}  

--------------------------------------------------

Database Tables

users  
sellers  
products  
product_images  
product_tags  
product_dimensions  
cart  
orders  

--------------------------------------------------

Run the Project

1. Install dependencies

pip install -r requirements.txt

2. Run the server

uvicorn app.main:app --reload

3. Open API Docs

http://127.0.0.1:8000/docs

--------------------------------------------------

## API Documentation

Swagger UI available at:

http://127.0.0.1:8000/docs

### Swagger Interface

![Swagger UI](images/swagger-ui.png)

--------------------------------------------------

Author

Shivam Malik
Backend Developer (Python / FastAPI)
