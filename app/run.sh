#!/bin/bash
# Port must match app.pdf-service.base-url in zarebin-backend's application.yml
uvicorn app.main:app --host 0.0.0.0 --port 8082
