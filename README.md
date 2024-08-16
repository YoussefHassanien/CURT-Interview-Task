# Inventory Management System

## Overview

This project is an Inventory Management System built using Flask for the backend, HTML/CSS for the frontend, and JavaScript for client-side functionality. The system allows users to register, login, and manage inventory items. Admin users have additional privileges to manage the inventory.

## Features

- User Registration and Login
- Password verification using SHA-256 hashing
- Inventory item management (add, edit, delete)
- Search functionality for inventory items
- Admin and general user roles

## Project Structure

- `app.py`: Main application file containing Flask routes and database interactions.
- `classes.py`: Contains class definitions for `User`, `Admin`, and various item types (`ElectricalPart`, `MechanicalPart`, `RawMaterial`).
- `templates/`: Directory containing HTML templates for different pages.
  - `register.html`: Registration page
  - `login.html`: Login page
  - `home.html`: Home page displaying inventory items
  - `admin.html`: Admin page for managing inventory items
- `static/`: Directory containing static files like CSS and JavaScript.
  - `CSS/styles.css`: Stylesheet for the application
  - `Scripts/script.js`: JavaScript file containing client-side functionality

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/inventory-management-system.git
    cd inventory-management-system
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database and update the connection details in `app.py`:
    ```python
    database_session = psycopg2.connect(
        database="your_database",
        port=5432,
        host="localhost",
        user="your_username",
        password="your_password"
    )
    ```

5. Run the application:
    ```sh
    flask run
    ```

## Usage

- Navigate to `http://localhost:5000` in your web browser.
- Register a new user or login with existing credentials.
- Admin users can manage inventory items by adding, editing, or deleting items.
- Use the search bar to filter inventory items.

## License

This project is licensed under the CUFE CURT License.