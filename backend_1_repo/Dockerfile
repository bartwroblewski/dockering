FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install ptvsd

COPY backend1.py .
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --multiprocess backend1.py
# ENTRYPOINT ["python", "backend1.py"]