# Inventory Management System (IMS)

A Flask-based inventory management system with MySQL database.

## Prerequisites

- Python 3.7 or higher
- MySQL Server installed and running
- pip (Python package manager)

## Setup Steps

### 1. Install Python Dependencies

Open a terminal in the project root directory (`E:\IMS`) and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask
- Flask-CORS
- mysql-connector-python

### 2. Configure MySQL Database (XAMPP)

1. **Start XAMPP** and make sure MySQL is running
2. The default configuration in `app/config.py` is already set for XAMPP:
   ```python
   DB_HOST = "localhost"
   DB_USER = "root"
   DB_PASSWORD = ""  # XAMPP default (no password)
   DB_NAME = "inventory_db"
   ```
3. If you've changed your XAMPP MySQL password, update `DB_PASSWORD` in `app/config.py`

### 3. Initialize the Database

Run the database initialization script to create the database and tables. You can run it from anywhere:

**Option 1: Direct execution (from project root)**
```bash
python app/database/init_db.py
```

**Option 2: Using Python module syntax (from project root)**
```bash
python -m app.database.init_db
```

This will:
- Create the `inventory_db` database if it doesn't exist
- Create the `products` table with the required schema

### 4. Run the Application

Start the Flask development server from the project root:

```bash
python app.py
```

The server will start on `http://localhost:5000` (or `http://0.0.0.0:5000`)

### 5. Access the Application

- **Web Interface**: Open your browser and go to `http://localhost:5000`
- **API Endpoints**:
  - `GET http://localhost:5000/products/` - Get all products
  - `POST http://localhost:5000/products/add` - Add a new product
  - `PUT http://localhost:5000/products/update/<id>` - Update a product
  - `DELETE http://localhost:5000/products/delete/<id>` - Delete a product
  - `GET http://localhost:5000/reports/stock-value` - Get total stock value

## API Usage Examples

### Add a Product
```bash
curl -X POST http://localhost:5000/products/add \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "quantity": 10}'
```

### Get All Products
```bash
curl http://localhost:5000/products/
```

### Update a Product
```bash
curl -X PUT http://localhost:5000/products/update/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop", "price": 1299.99, "quantity": 5}'
```

### Delete a Product
```bash
curl -X DELETE http://localhost:5000/products/delete/1
```

### Get Stock Value
```bash
curl http://localhost:5000/reports/stock-value
```

## Troubleshooting

1. **MySQL Connection Error**: 
   - Ensure MySQL Server is running
   - Check your credentials in `app/config.py`
   - Verify MySQL is accessible on the specified host

2. **Module Not Found Error**:
   - Make sure you've installed all dependencies: `pip install -r requirements.txt`
   - Verify you're using the correct Python environment

3. **Port Already in Use**:
   - Change the port in `app.py` from `5000` to another port (e.g., `5001`)
   - Or stop the process using port 5000

## Project Structure

```
inventory_system/
│
├── app/
│   ├── database/
│   │   ├── connection.py
│   │   └── init_db.py
│   │
│   ├── routers/
│   │   ├── products.py
│   │   └── reports.py
│   │
│   ├── schemas/
│   │   └── inventory_schema.py
│   │
│   ├── static/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   │
│   ├── config.py
│   ├── main.py
│   └── __init__.py
│
├── README.md
├── requirements.txt
├── app.py                  # Application entry point (run this)
└── .gitignore
```
