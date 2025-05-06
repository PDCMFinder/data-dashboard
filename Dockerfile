# Stage 1: Build wheels
FROM python:3.9.6-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y \
    git gcc g++ python3-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*  # Reduce image size
COPY requirements.txt .
RUN pip install wheel
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

# Stage 2: Install from wheels
FROM python:3.9.6-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt && pip install --no-cache-dir git+https://github.com/hshhrr/plotly-upset.git
COPY . .
EXPOSE 8050/tcp
CMD ["python", "main.py"]
