FROM python:3.12-slim
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends gdal-bin \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ingest_pilot.py .
COPY build_delivery.py .
COPY test_ingest_pilot.py .
COPY input ./input
CMD ["python", "ingest_pilot.py"]
