# Simple Store — Django E-commerce Demo

A basic e-commerce site built with **Django** (backend) and plain **HTML/CSS**
(templates). Includes product listings, product detail pages, a shopping cart,
order processing/checkout, and user registration/login.

## Features

- **Product listings** with category filter and search
- **Product detail page** with stock display and "add to cart"
- **Shopping cart** (works for logged-out visitors too, via session; merges
  naturally once you're used to it — see "How the cart works" below)
- **Order processing / checkout**: collects shipping info, validates stock,
  creates an `Order` + `OrderItem`s, decrements stock, empties the cart
- **User registration/login/logout** using Django's built-in auth
- **Order history** page for logged-in users
- **Database**: SQLite by default (products, users, carts, orders — all as
  proper Django models), with a Django admin panel to manage everything
- **Sample data seeder** so you have products to click around with immediately

## Project structure

```
ecommerce_project/
├── manage.py
├── requirements.txt
├── ecommerce/          # project settings, root urls
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── store/              # the app with all the e-commerce logic
    ├── models.py        # Category, Product, Cart, CartItem, Order, OrderItem
    ├── views.py          # product list/detail, cart, checkout, auth
    ├── urls.py
    ├── forms.py           # RegisterForm, CheckoutForm
    ├── admin.py
    ├── management/commands/seed_products.py   # sample data
    ├── templates/store/   # product_list, product_detail, cart, checkout...
    ├── templates/registration/  # login, register
    └── static/store/css/style.css
```

## Setup (run locally)

You'll need **Python 3.10+** installed.

```bash
# 1. Unzip and enter the project
cd ecommerce_project

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install Django
pip install -r requirements.txt

# 4. Create the database tables
python manage.py makemigrations
python manage.py migrate

# 5. (optional) create an admin superuser, to log in at /admin/
python manage.py createsuperuser

# 6. Load some sample products so the store isn't empty
python manage.py seed_products

# 7. Run the dev server
python manage.py runserver
```

Then visit:
- **http://127.0.0.1:8000/** — the store
- **http://127.0.0.1:8000/admin/** — Django admin (manage products, orders, users)

## How it works

- **Product listings** (`/`): `product_list` view queries active `Product`s,
  supports `?category=<slug>` and `?q=<search>`.
- **Product detail** (`/product/<slug>/`): shows stock, price, description, and
  an "Add to Cart" form.
- **Cart** (`/cart/`): each visitor gets a `Cart` — tied to their `User` if
  logged in, or to their anonymous session otherwise (`get_cart()` in
  `views.py` handles this). Add/update/remove all go through simple POST
  endpoints.
- **Checkout** (`/checkout/`, login required): validates stock is still
  available, then in one atomic transaction creates the `Order`, snapshots
  each cart line into an `OrderItem` (so price/name are frozen even if the
  product changes later), decrements product stock, and empties the cart.
- **Order processing status**: orders are marked `paid` immediately (payment
  is simulated — there's no real payment gateway). You could swap this for a
  real integration (e.g. Stripe) by calling out to their API inside
  `checkout()` before setting the status.
- **Auth**: registration uses Django's `UserCreationForm` (subclassed to add
  an email field); login/logout use Django's built-in auth views.

## Where to extend this

- Add product images properly (an `ImageField` + media uploads) instead of
  the `image_url` link field
- Add pagination to the product list
- Hook up a real payment processor (Stripe/PayPal) in `checkout()`
- Add product reviews/ratings
- Add an "edit profile" / address book so checkout can pre-fill
- Switch `DATABASES` to Postgres for production, and set a real `SECRET_KEY`
  + `DEBUG = False` + proper `ALLOWED_HOSTS` before deploying
