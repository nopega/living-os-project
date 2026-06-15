FROM python:3.9.6-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# install deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =========================
# cd เข้า pipelines
# =========================
WORKDIR /app/pipelines

COPY pipelines .

# run เหมือนอยู่ใน pipelines แล้ว
CMD ["python", "flow.py"]