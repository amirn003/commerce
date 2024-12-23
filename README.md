# Commerce Django (HarvardX)

This is a Django-based web application for managing auctions. Users can create, bid on, and comment on auction listings.

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/amirn003/commerce-harvardx-project2.git
    cd commerce
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Apply migrations:**
    ```sh
    python3 manage.py migrate
    ```

4. **Run the development server:**
    ```sh
    python3 manage.py runserver
    ```

## Configuration

### ASGI

The ASGI configuration is located in `commerce/asgi.py`.

### WSGI

The WSGI configuration is located in `commerce/wsgi.py`.

### URLs

The URL configuration is located in `commerce/urls.py`.

### Settings

The settings for the project are located in `commerce/settings.py`.

## Usage

- Access the admin interface at `/admin/`.
- The main auction functionalities are available at the root URL (`/`).

## Deployment

This project is configured to be deployed on Heroku. Ensure you have the Heroku CLI installed and follow these steps:

1. **Login to Heroku:**
    ```sh
    heroku login
    ```

2. **Create a new Heroku app:**
    ```sh
    heroku create
    ```

3. **Deploy the app:**
    ```sh
    git push heroku main
    ```

4. **Run migrations on Heroku:**
    ```sh
    heroku run python3 manage.py migrate
    ```
