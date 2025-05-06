# product-service/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install --no-cache-dir Flask
# Port mà Flask app lắng nghe bên trong container
EXPOSE 5001
# Có thể set API Key mặc định ở đây nếu muốn
# ENV PRODUCT_SERVICE_API_KEY=supersecretkey
CMD ["python", "app.py"]
