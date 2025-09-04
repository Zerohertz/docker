curl -X 'POST' \
    'http://localhost:${FASTAPI_PORT}/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
            "file_id": ""
        }'