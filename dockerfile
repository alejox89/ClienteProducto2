# Iniciar Pull del a imagen.
FROM python:3.8.3-slim

# Ejeutar comandos sobre la imagen instalada
# RUN apt-get update \
#     && apt-get -y install libpq-dev gcc \
#     && pip install psycopg2

# Copiar los requisistos
COPY ./requirements.txt /app/requierement.txt

# Cambiar el directorio de trabajo
WORKDIR /app

# Instalar dependencias
RUN pip install -r requierement.txt

# Copiar informacion
COPY src/ /app/

# Configurar comando de ejecucion
#ENTRYPOINT [ "python" ]

# Exponer puerto 5000
EXPOSE 8000

# Ejecutar la aplicacion
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8090"]