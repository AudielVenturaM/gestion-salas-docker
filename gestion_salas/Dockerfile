# Usamos una imagen oficial de Python como base
FROM python:3.10-slim

# Establecemos variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Creamos y establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos
COPY requirements.txt /app/

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código del proyecto al contenedor
COPY . /app/

# El puerto que el contenedor expondrá
EXPOSE 8000

# El comando para iniciar la aplicación cuando el contenedor se ejecute
# Usaremos Gunicorn, un servidor de aplicaciones Python para producción
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]