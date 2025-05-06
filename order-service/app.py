# order-service/app.py
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Lấy URL của product-service từ biến môi trường
PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://product-service:5001")
# Lấy API Key để gọi product-service từ biến môi trường
PRODUCT_SERVICE_API_KEY = os.environ.get("PRODUCT_SERVICE_API_KEY", "supersecretkey")

ORDERS = [] # Lưu trữ đơn hàng đơn giản

@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing product_id or quantity"}), 400

    product_id = data['product_id']
    quantity_needed = data['quantity']

    print(f"Received order for {quantity_needed} of {product_id}. Fetching product details...")

    # --- Gọi API của product-service (Data & Security Integration) ---
    try:
        product_url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"
        headers = {
            'X-API-KEY': PRODUCT_SERVICE_API_KEY # Gửi kèm API Key
        }
        print(f"Calling Product Service at {product_url} with API Key.")
        # Đặt timeout để tránh chờ đợi vô hạn
        response = requests.get(product_url, headers=headers, timeout=3.0) # Timeout 3 giây

        # Xử lý lỗi HTTP từ product-service
        if response.status_code == 401:
            print("Error: API Key rejected by Product Service.")
            return jsonify({"error": "Internal configuration error - Failed to authenticate with Product Service"}), 500
        elif response.status_code == 404:
            print(f"Error: Product {product_id} not found in Product Service.")
            return jsonify({"status": "Order rejected", "reason": "Product not found"}), 400
        
        # Ném exception cho các lỗi 4xx, 5xx khác (ngoại trừ 401, 404 đã xử lý)
        response.raise_for_status() 

        # Xử lý dữ liệu trả về thành công (Data Integration Aspect)
        product_data = response.json()
        print(f"Product data received: {product_data}")

        # Kiểm tra cấu trúc dữ liệu trả về có đúng như mong đợi không
        # Lưu ý tên key trả về từ product-service: product_name, current_price, quantity_available
        product_name = product_data.get("product_name")
        price = product_data.get("current_price")
        stock = product_data.get("quantity_available")

        if product_name is None or price is None or stock is None:
             print("Error: Unexpected data structure received from Product Service.")
             return jsonify({"error": "Internal error - Inconsistent data from Product Service"}), 500

        # Kiểm tra tồn kho
        if stock >= quantity_needed:
            # Tạo đơn hàng (giả lập)
            order_id = len(ORDERS) + 1
            order = {
                "id": order_id,
                "product_id": product_id,
                "product_name": product_name, # Lưu tên lấy được
                "quantity": quantity_needed,
                "total_price": round(price * quantity_needed, 2),
                "status": "confirmed"
            }
            ORDERS.append(order)
            print(f"Order {order_id} confirmed.")
            return jsonify({"status": "Order confirmed", "order": order}), 200
        else:
            print(f"Insufficient stock for {product_id}. Needed: {quantity_needed}, Available: {stock}")
            return jsonify({"status": "Order rejected", "reason": "Insufficient stock"}), 400

    except requests.exceptions.Timeout:
        print("Error: Product service timed out.")
        return jsonify({"error": "Product service timed out. Please try again later."}), 504 # Gateway Timeout
    except requests.exceptions.RequestException as e:
        print(f"Error calling product service: {e}")
        return jsonify({"error": f"Product service unavailable: {e}"}), 503 # Service Unavailable
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected internal error occurred"}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(ORDERS), 200

if __name__ == "__main__":
    print("Order Service starting...")
    # Chạy trên port 5353 trong container
    app.run(host='0.0.0.0', port=5353, debug=True)
