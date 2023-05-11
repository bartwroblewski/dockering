FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend1.py .
ENTRYPOINT ["python", "backend1.py"]