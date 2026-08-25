# ShopEase 🛍️

ShopEase is a basic e-commerce web application developed using Django as part of my Full Stack Development Task 1.

The project focuses on building a simple online shopping experience where users can browse products, view product details, manage their shopping cart and place orders.

## Features

- Product listing with images
- Product details page
- User registration and login
- Add products to cart
- Increase or decrease product quantity
- Remove products from cart
- Checkout and order placement
- Order confirmation
- Product and order management through Django Admin
- SQLite database for storing application data

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Django
- **Database:** SQLite

## Project Structure

```text
ShopEase/
├── manage.py
├── ShopEase/
├── store/
├── templates/
├── media/
└── db.sqlite3

How to Run:

1.Install the required packages:
pip install django pillow

2.Run the database migrations:
python manage.py migrate

3.Start the Django development server:
python manage.py runserver

4.Open the application in your browser:
http://127.0.0.1:8000/

**About the Project:
This project helped me understand how a full-stack web application works by connecting the frontend with Django backend functionality and a database. It also gave me practical experience with authentication, product management, shopping cart functionality and order processing.
