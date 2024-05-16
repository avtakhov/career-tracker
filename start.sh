#!/bin/bash

if [ "$ENVIRONMENT" = "local" ]; then
  uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload --ssl-keyfile ./env/ssl.pem --ssl-certfile ./env/ssl.crt
else
  uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 4 --ssl-keyfile ./env/ssl.pem --ssl-certfile ./env/ssl.crt
fi
