FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install ptvsd

COPY backend1.py .
# CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m python backend1.py -h 0.0.0 -p 5000
ENTRYPOINT ["python", "backend1.py"]