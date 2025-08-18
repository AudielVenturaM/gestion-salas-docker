\# Sistema de Gestión de Salas de Juntas



Una aplicación web full-stack para la administración y reservación de salas de juntas, construida con Django y Vue.js, y completamente containerizada con Docker.



---



\## 🚀 Características Principales



\* \*\*Gestión de Salas (CRUD):\*\* Creación, visualización, actualización y eliminación de salas de juntas a través de una API REST.

\* \*\*Sistema de Reservaciones:\*\* Permite a los usuarios reservar una sala especificando un rango de horario.

\* \*\*Validaciones de Negocio:\*\*

&nbsp;   \* Impide la reservación de salas en horarios que se solapan.

&nbsp;   \* Limita la duración máxima de una reservación a 2 horas.

\* \*\*Liberación Manual:\*\* Opción para cancelar una reservación antes de su hora de finalización.

\* \*\*Liberación Automática:\*\* Las reservaciones terminadas desaparecen de la lista de "próximas".

\* \*\*Interfaz Reactiva:\*\* Frontend construido como una Single Page Application (SPA) con Vue.js.

\* \*\*Entorno Containerizado:\*\* Toda la aplicación (Backend, Frontend, Base de Datos) se ejecuta en contenedores Docker para un despliegue y desarrollo consistentes.



---



\## 🛠️ Tecnologías Utilizadas



\* \*\*Backend:\*\* Python, Django, Django REST Framework

\* \*\*Frontend:\*\* JavaScript, Vue.js, Vite

\* \*\*Base de Datos:\*\* PostgreSQL

\* \*\*Servidor Web (Frontend):\*\* Nginx (configurado como Reverse Proxy)

\* \*\*Containerización:\*\* Docker, Docker Compose

\* \*\*Control de Versiones:\*\* Git



---



\## 📦 Prerrequisitos



Para ejecutar este proyecto, necesitas tener instalado:



\* \[Git](https://git-scm.com/)

\* \[Docker Desktop](https://www.docker.com/products/docker-desktop/)



---



\## ⚙️ Instalación y Ejecución



Gracias a la configuración de Docker Compose, levantar el proyecto es un proceso de un solo comando.



1\.  \*\*Clona el repositorio\*\*:

&nbsp;   ```bash

&nbsp;   git clone https://github.com/AudielVenturaM/gestion-salas-docker

&nbsp;   cd gestion-salas-docker

&nbsp;   ```

&nbsp;   \*Si solo tienes la carpeta, simplemente navega a la raíz del proyecto (`proyecto-docker`).\*



2\.  \*\*Construye e inicia los contenedores:\*\*

&nbsp;   Este comando leerá el archivo `docker-compose.yml`, construirá las imágenes de tus aplicaciones y las iniciará.

&nbsp;   ```bash

&nbsp;   docker-compose up --build

&nbsp;   ```

&nbsp;   \*La primera vez puede tardar varios minutos mientras se descargan las imágenes base.\*



3\.  \*\*Prepara la base de datos (en una segunda terminal):\*\*

&nbsp;   Mientras la aplicación está corriendo, abre **otra terminal** en la misma carpeta y ejecuta los siguientes comandos para configurar la base de datos por primera vez:

&nbsp;   ```bash
&nbsp;	# Crear las tablas en la base de datos

&nbsp;   docker-compose exec backend python manage.py migrate

&nbsp;   ```



4\.  \*\*Crea un superusuario\*\* para acceder al panel de administrador de Django (opcional):

&nbsp;   ```bash

&nbsp;   docker-compose exec backend python manage.py createsuperuser

&nbsp;   ```



5\.  \*\*¡Accede a la aplicación!\*\*

&nbsp;   \* \*\*Frontend (Aplicación Principal):\*\* Abre tu navegador y ve a `http://localhost:5173`

&nbsp;   \* \*\*Backend (Admin de Django):\*\* `http://localhost:8000/admin/`



---

---

### Cómo Detener la Aplicación

Para detener todos los contenedores, simplemente presiona `Ctrl + C` en la terminal donde ejecutaste `docker-compose up`.

---



\## 📝 Endpoints de la API



La API REST del backend expone los siguientes endpoints principales:



| Método | URL                                       | Descripción                               |

| :----- | :---------------------------------------- | :---------------------------------------- |

| `GET`  | `/api/rooms/`                             | Obtiene la lista de todas las salas.      |

| `POST` | `/api/rooms/`                             | Crea una nueva sala.                      |

| `GET`  | `/api/rooms/<id>/`                        | Obtiene los detalles de una sala.         |

| `GET`  | `/api/rooms/<id>/reservations/`           | Obtiene las reservaciones de una sala.    |

| `POST` | `/api/rooms/<id>/reservations/`           | Crea una nueva reservación para una sala. |

| `DELETE`| `/api/reservations/<id>/delete/`        | Elimina una reservación específica.       |



---



\## 🧑‍💻 Autor



\* \*\*Audiel Ventura Marrufo\*\* - audiel654@gmail.com - www.linkedin.com/in/audiel-ventura-marrufo-a873b82b0 - https://github.com/AudielVenturaM/gestion-salas-docker



