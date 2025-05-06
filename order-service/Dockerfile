# order-service/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install --no-cache-dir Flask requests
# Port mà Flask app lắng nghe bên trong container
EXPOSE 5353
# Biến môi trường mặc định (sẽ được ghi đè bởi docker-compose)
ENV PRODUCT_SERVICE_URL=http://product-service:5001
ENV PRODUCT_SERVICE_API_KEY=supersecretkey
CMD ["python", "app.py"]