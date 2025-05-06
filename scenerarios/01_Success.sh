#!/bin/sh

curl -X POST -H "Content-Type: application/json" \
-d '{"product_id": "prod_001", "quantity": 5}' \
http://localhost:5353/create-order
