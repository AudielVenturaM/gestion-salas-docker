# --- Etapa de Construcción (Build Stage) ---
# Usamos una imagen de Node.js para construir nuestro proyecto
FROM node:20-alpine as build-stage

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de definición del proyecto
COPY package*.json ./

# Instalamos las dependencias
RUN npm install

# Copiamos todo el código del frontend
COPY . .

# Construimos la versión de producción (archivos estáticos optimizados)
RUN npm run build

# --- Etapa de Producción (Production Stage) ---
# Usamos una imagen de Nginx, un servidor web ligero y eficiente
FROM nginx:stable-alpine as production-stage

# Copiamos los archivos construidos de la etapa anterior
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Definimos las reglas de Nginx
COPY nginx.conf etc/nginx/conf.d/default.conf

# Exponemos el puerto 80, que es el puerto por defecto de Nginx
EXPOSE 80

# El comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]