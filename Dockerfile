# 1. Imagen base ligera con Python 3.11 en Linux
FROM python:3.11-slim

# 2. Evita que Python escriba archivos .pyc y fuerza la salida directa de logs a la terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema necesarias para gráficos (Matplotlib/Seaborn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar e instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# 6. Copiar todo el código fuente del proyecto al contenedor
COPY . .

# 7. Comando por defecto para ejecutar el pipeline de viáticos
CMD ["python", "main.py"]