# Online Food Delivery System API

A Django REST API for an online food delivery system that connects customers, restaurants, and delivery personnel.

## Features

- Custom User Authentication System with JWT
- Multiple User Types (Customer, Restaurant Owner, Delivery Person)
- Restaurant Management
- Menu Management
- Order Processing System
- User Profile Management

## Tech Stack
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication (Simple JWT)
- Djoser


## Installation

1. Clone the repository
3. Create a virtual environment
3. Activate the virtual environment
4. Install dependencies
5. Create a `.env` file in the root
6. Run migrations
7. Create a superuser
8. Run the development server

## API Endpoints

### Authentication

- `POST /auth/jwt/create/` - Obtain JWT token
- `POST /auth/jwt/refresh/` - Refresh JWT token
- `POST /auth/users/` - Register new user

### User Management
- `GET /api/users/` - List all users (Public profiles)
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Restaurant Management

- `GET /api/restaurants/` - List all restaurants
- `POST /api/restaurants/` - Create new restaurant (Restaurant owners only)
- `GET /api/restaurants/{id}/` - Get restaurant details
- `PUT /api/restaurants/{id}/` - Update restaurant (Owner only)
- `DELETE /api/restaurants/{id}/` - Delete restaurant (Owner only)

### Menu Management

- `GET /api/restaurants/{restaurant_id}/menu-items/` - List menu items
- `POST /api/restaurants/{restaurant_id}/menu-items/` - Add menu item (Owner only)
- `PUT /api/restaurants/{restaurant_id}/menu-items/{id}/` - Update menu item (Owner only)
- `DELETE /api/restaurants/{restaurant_id}/menu-items/{id}/` - Delete menu item (Owner only)

### Order Management

- `GET /api/orders/` - List orders (Customer sees own orders, Restaurant sees their orders)
- `POST /api/orders/` - Create new order (Customers only)
- `GET /api/orders/{id}/` - Get order details
- `PUT /api/orders/{id}/` - Update order
- status (Restaurant owners only)

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```bash
Authorization: Bearer <your_token>
```

To obtain a token:
```bash
curl -X POST http://localhost:8000/auth/jwt/create/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "your_password"}'
```
# User Types

1. Customer
   - Can browse restaurants
   - Can place orders
   - Can view order history

2. Restaurant Owner
   - Can manage restaurant profile
   - Can manage menu items
   - Can process orders

3. Delivery Person
   - Can view assigned deliveries
   - Can update delivery status

