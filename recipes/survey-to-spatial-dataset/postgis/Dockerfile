FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ingest_pilot.py .
COPY input ./input
CMD ["python", "ingest_pilot.py"]
