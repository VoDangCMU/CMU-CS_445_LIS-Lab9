# product-service/app.py
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# API Key tĩnh đơn giản (trong thực tế nên dùng cơ chế phức tạp hơn)
# Lấy từ biến môi trường hoặc dùng giá trị mặc định
EXPECTED_API_KEY = os.environ.get("PRODUCT_SERVICE_API_KEY", "supersecretkey")

# Dữ liệu sản phẩm giả lập
PRODUCTS = {
    "prod_001": {"id": "prod_001", "name": "Laptop Model X", "price": 1250.75, "stock": 15},
    "prod_002": {"id": "prod_002", "name": "Wireless Mouse", "price": 25.99, "stock": 50},
    "prod_003": {"id": "prod_003", "name": "Mechanical Keyboard", "price": 89.50, "stock": 0}, # Hết hàng
}

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    # --- Security Check ---
    api_key = request.headers.get('X-API-KEY')
    if not api_key or api_key != EXPECTED_API_KEY:
        print(f"Unauthorized access attempt with key: {api_key}")
        return jsonify({"error": "Unauthorized"}), 401 # Lỗi 401 Unauthorized

    # --- Data Retrieval ---
    print(f"Received authorized request for product: {product_id}")
    product = PRODUCTS.get(product_id)

    if product:
        print(f"Product found: {product}")
        # Trả về dữ liệu với cấu trúc nhất quán
        return jsonify({
            "id": product["id"],
            "product_name": product["name"], # Đổi tên key để minh họa
            "current_price": product["price"],
            "quantity_available": product["stock"]
        }), 200
    else:
        print(f"Product {product_id} not found.")
        return jsonify({"error": "Product not found"}), 404 # Lỗi 404 Not Found

if __name__ == "__main__":
    print("Product Service starting...")
    # Chạy trên port 5001 trong container
    app.run(host='0.0.0.0', port=5001, debug=True)
