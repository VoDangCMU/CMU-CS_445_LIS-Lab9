#!/bin/sh

curl -X POST -H "Content-Type: application/json" \
-d '{"product_id": "prod_invalid", "quantity": 1}' \
http://localhost:5353/create-order
