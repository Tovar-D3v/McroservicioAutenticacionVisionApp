# Usa la imagen oficial de Python
FROM python:3.11-slim 

# Establece el directorio de trabajo
WORKDIR .

# Instala las dependencias del sistema necesarias para OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0  \
    pkg-config \
    default-libmysqlclient-dev\
    libpq-dev build-essential \
    gcc

# Evita archivos .pyc y buffer en stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Actualiza pip y cachea dependencias
RUN pip install --upgrade pip

# Copia solo los archivos de dependencias primero (mejora caché)
COPY requirements.txt .
# Instala las dependencias (optimizado con caché)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto (opcional, solo informativo)
EXPOSE 8064
EXPOSE 8064

# Comando de ejecución
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8064"]