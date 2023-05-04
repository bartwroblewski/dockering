FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend2.py .
ENTRYPOINT ["uvicorn", "backend2:app", "--host", "0.0.0.0", "--reload"]