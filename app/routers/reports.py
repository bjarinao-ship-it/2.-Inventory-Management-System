from flask import Blueprint, jsonify
from app.database.connection import get_db
import mysql.connector

reports_router = Blueprint("reports", __name__)

@reports_router.get("/stock-value")
def stock_value():
    try:
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute("SELECT SUM(price * quantity) FROM products")
            result = cursor.fetchone()
            total_value = float(result[0]) if result[0] else 0.0
            return jsonify({"total_stock_value": total_value}), 200
        finally:
            cursor.close()
            db.close()
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500
