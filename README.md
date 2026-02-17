# 🛍️ ShopNest - Single Vendor E-Commerce Platform

A full-featured, modern single-vendor e-commerce platform built with Django. ShopNest provides a complete online shopping experience with product management, shopping cart, secure payment integration, and user authentication.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)


## 🌟 Features

### 🔐 Authentication & User Management
- **User Registration & Login** - Custom authentication with username/email
- **Social Authentication** - Google OAuth integration using Django Allauth
- **Session Management** - Persistent user sessions with automatic login redirect
- **Profile Management** - User profile with order history and account details

### 📦 Product Management
- **Product Catalog** - Browse products with detailed information
- **Category Organization** - Products organized by categories with slug-based URLs
- **Product Search** - Advanced search across product names, descriptions, and categories
- **Product Images** - Image upload with date-based organization
- **Stock Management** - Real-time inventory tracking
- **Related Products** - Automatic display of products in the same category

### ⭐ Product Reviews & Ratings
- **5-Star Rating System** - Rate products from 1 to 5 stars
- **Review Comments** - Leave detailed feedback on purchased products
- **Average Rating Display** - Automatic calculation and display of average ratings
- **Purchase Verification** - Only buyers can rate products they've purchased
- **Edit Ratings** - Update your existing ratings and reviews

### 🛒 Shopping Cart
- **Persistent Cart** - Cart saved per user account
- **Real-time Updates** - Instant quantity adjustments
- **Stock Validation** - Prevents adding more items than available stock
- **Cart Summary** - Total items and cost calculation
- **Quantity Control** - Increase/decrease quantities or remove items
- **Session-based** - Cart persists across sessions for logged-in users

### 💳 Checkout & Payment
- **Secure Checkout** - Multi-step checkout process
- **Guest Information** - Ship to different addresses with custom recipient details
- **SSLCommerz Integration** - Secure payment gateway for Bangladesh market
- **Payment Status Tracking** - Success, failure, and cancellation handling
- **Order Confirmation** - Email notifications upon successful payment
- **Transaction Management** - Unique transaction IDs for each order

### 📊 Order Management
- **Order History** - View all past orders in user profile
- **Order Status Tracking** - Real-time order status updates
  - Pending
  - Processing
  - Shipped
  - Delivered
  - Canceled
- **Order Details** - Itemized breakdown with quantities and prices
- **Total Spent** - Lifetime purchase analytics

### 🔍 Advanced Filtering & Search
- **Multi-criteria Filtering**
  - Filter by category
  - Price range filtering (min/max)
  - Rating-based filtering
- **Smart Search** - Search across product names, descriptions, and categories
- **Dynamic Price Range** - Auto-calculated min/max price boundaries

### 📧 Email Notifications
- **Order Confirmations** - HTML email templates for order confirmation
- **Custom Email Templates** - Professional, branded email designs

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 6.0
- **Database**: SQLite (development) / PostgreSQL-ready
- **Authentication**: Django Allauth
- **Payment Gateway**: SSLCommerz

### Frontend
- **Template Engine**: Django Templates
- **Styling**: Tailwind CSS (utility-first, CDN)
- **Icons**: Font Awesome
- **Image Handling**: Pillow (PIL)


## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- SSLCommerz merchant account (for payment integration)
- Email account for SMTP (Gmail, SendGrid, etc.)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/shopnest.git
cd ShopNest
```

### 2. Create Virtual Environment
```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the `ShopNest` directory (inner folder) with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (if using PostgreSQL)
DATABASE_URL=postgres://user:password@localhost:5432/shopnest

# SSLCommerz Payment Gateway
SSLCOMMERZ_STORE_ID=your_store_id
SSLCOMMERZ_STORE_PASSWORD=your_store_password
SSLCOMMERZ_PAYMENT_URL=https://sandbox.sslcommerz.com/gwprocess/v4/api.php
SSLCOMMERZ_VALIDATION_URL=https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### 5. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

```bash
ShopNest/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── Model_deatils.md
├── .env
├── media/                          # User uploaded files
│   └── products/
│       └── YYYY/MM/DD/             # Date-based organization
├── static/                         # Static assets (images, welcome.png)
├── templates/                      # HTML templates
│   ├── base.html
│   └── shop/
│       ├── home.html
│       ├── product_list.html
│       ├── product_detail.html
│       ├── cart.html
│       ├── checkout.html
│       ├── profile.html
│       ├── login.html
│       ├── register.html
│       ├── rate_product.html
│       ├── payment_success.html
│       ├── payment_fail.html
│       ├── payment_cancel.html
│       └── email/
│           └── order_confirmation.html
├── shop/                           # Main application
│   ├── models.py                   # Database models
│   ├── views.py                    # View logic
│   ├── urls.py                     # URL routing
│   ├── forms.py                    # Django forms
│   ├── admin.py                    # Admin configuration
│   ├── sslcommerz.py               # Payment integration
│   ├── context_processor.py        # Custom context processors
│   └── migrations/
└── ShopNest/                       # Project configuration
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

## 💾 Database Models

### Core Models

#### **Category**
- Organizes products into categories
- Slug-based URLs for SEO
- One-to-many relationship with Products

#### **Product**
- Complete product information (name, description, price)
- Stock management with availability status
- Image storage with date-based organization
- Automatic timestamp tracking
- Average rating calculation

#### **Rating**
- 1-5 star rating system
- Text comments/reviews
- Links users to products
- Timestamp tracking

#### **Cart & CartItem**
- One cart per user (OneToOne)
- Multiple items per cart
- Automatic total price calculation
- Quantity management

#### **Order & OrderItem**
- Complete order information
- Shipping details
- Payment status tracking
- Order status workflow
- Email notifications

  
## Admin Features

- **Django Admin Panel** - Full CRUD operations
- **Category Management** - Create and organize categories
- **Product Management** - Add products with images
- **Order Management** - View and update order status
- **User Management** - Manage customer accounts
- **Stock Control** - Monitor and update inventory

## 🔒 Security Features

- CSRF protection on all forms
- Password validation and hashing
- Login required decorators
- Purchase verification for ratings
- Secure payment gateway integration
- Environment variables for sensitive data
- Session security

## 📧 Email Configuration

The platform sends HTML emails for:
- Order confirmations with itemized details
- Custom branded templates

Configure your SMTP settings in `.env` file. For Gmail:
1. Enable 2-factor authentication
2. Generate an app-specific password
3. Use the app password in EMAIL_HOST_PASSWORD

## 🌐 Deployment

### Render.com Deployment
The project is configured for deployment on Render.com:
- Production URL: `https://shopnest-4thm.onrender.com`
- CSRF trusted origins configured
- Static files configuration ready



## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- GitHub: [@nabil0203](https://github.com/nabil0203)
- Email: nabilahmed0203@gmail.com

## 🙏 Acknowledgments

- Django Framework Documentation
- SSLCommerz for payment gateway
- Django Allauth for social authentication
- Tailwind CSS for styling and responsive design
