#syntax=docker/dockerfile:1
FROM python:3.13-slim

#Evita prompts y bajamos ruido
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

#Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependencias Python primero
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia el código fuente del proyecto (sin data)
COPY src /app/src
COPY docs /app/docs
COPY README.md /app/README.md

# Crea directorios esperados
RUN mkdir -p /app/reports/figures /app/reports/tables /app/data/staging

# Comando por defecto: ejecutar insights
CMD ["python", "-m", "src.analytics.insights"]
