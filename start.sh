#!/bin/bash

curl -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/setWebhook" -d "url=${WEBHOOK_URL}"

if [ "$ENVIRONMENT" = "local" ]; then
  uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
else
  uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 4 --ssl-keyfile ./env/ssl.pem --ssl-certfile ./env/ssl.crt
fi
