from flask import Flask, send_from_directory
from flask_cors import CORS
from app.routers.products import products_router
from app.routers.reports import reports_router

app = Flask(__name__, static_folder='app/static', static_url_path='')
CORS(app)

app.register_blueprint(products_router, url_prefix="/products")
app.register_blueprint(reports_router, url_prefix="/reports")

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

