from flask import Blueprint, request, jsonify
from app.database.connection import get_db
from app.schemas.inventory_schema import ProductSchema
import mysql.connector

products_router = Blueprint("products", __name__)

# ADD PRODUCT
@products_router.post("/add")
def add_product():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        product = ProductSchema(**data)
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
                (product.name, product.price, product.quantity)
            )
            db.commit()
            return jsonify({"message": "Product added successfully"}), 201
        finally:
            cursor.close()
            db.close()
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 400

# VIEW ALL
@products_router.get("/")
def get_products():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            return jsonify(products), 200
        finally:
            cursor.close()
            db.close()
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

# UPDATE
@products_router.put("/update/<int:id>")
def update_product(id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute("""
                UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s
            """, (data["name"], data["price"], data["quantity"], id))
            
            if cursor.rowcount == 0:
                return jsonify({"error": "Product not found"}), 404
            
            db.commit()
            return jsonify({"message": "Product updated successfully"}), 200
        finally:
            cursor.close()
            db.close()
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 400

# DELETE
@products_router.delete("/delete/<int:id>")
def delete_product(id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute("DELETE FROM products WHERE id=%s", (id,))
            
            if cursor.rowcount == 0:
                return jsonify({"error": "Product not found"}), 404
            
            db.commit()
            return jsonify({"message": "Product deleted"}), 200
        finally:
            cursor.close()
            db.close()
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500
