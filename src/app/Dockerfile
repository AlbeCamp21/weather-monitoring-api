# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Copiar requirements
COPY ../../requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim as production

WORKDIR /app

# Copiar dependencias instaladas desde el stage anterior
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]