# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo los archivos de requerimientos e instálalos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Expone el puerto de la app (Flask usará el 5000)
EXPOSE 5000

# Variable para permitir conexiones externas en Flask (por si usas `flask run`)
ENV FLASK_RUN_HOST=0.0.0.0

# Comando por defecto con Gunicorn (más robusto para producción)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
