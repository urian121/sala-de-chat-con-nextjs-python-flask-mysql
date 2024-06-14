# Sala de Chat con Next.js, Python, Flask y MySQL

#### Pasos

##### Crear tu entorno virtual, ejecutando

    virtualenv env
    Activas tu entorno virtual

    . env/Scripts/activate

##### Crear el archivo requirements.txt

    pip freeze > requirements.txt

#### Instalar paquetes necesarios en el entorno virtual

##### Instala el framework Flask

    pip install flask

##### Instala el paquete requests para realizar solicitudes HTTP

    pip install requests

##### Instala el paquete Flask-JWT-Extended

    pip install flask-jwt-extended

##### Instala el paquete mysql-connector-python para la base de datos MySQL

    pip install mysql-connector-python

##### Instala Pillow para la manipulación de imagenes

    pip install pillow

##### Instalación de Flask-CORS

    pip install flask-cors

##### Instalación de Flask-SocketIO

    pip install flask-socketio

##### Generar archivo requirements.txt

    pip freeze > requirements.txt

##### Instalar todos las dependencias del proyecto

    pip install -r requirements.txt

##### Flask-JWT-Extended: Este es uno de los paquetes más completos y fáciles de usar para la implementación de JWT en Flask. Proporciona muchas funcionalidades, como el manejo de acceso basado en roles, refresco de tokens, y más.

- Validar el peso y la extension de foto en el front

##### Paso 2: Obtener el Token JWT

    Utiliza una herramienta como Postman para enviar una solicitud POST al endpoint /login con el siguiente cuerpo JSON:
    {
        "username": "test",
        "password": "test"
    }

##### Recibirás un token JWT en la respuesta. Por ejemplo:

    {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}

##### Paso 3: Acceder a la Ruta Protegida

    Usa el token JWT recibido para hacer una solicitud GET al endpoint /api. Añade el token en el encabezado de autorización:
    Authorization: Bearer <your-jwt-token>

##### Resumen

    Instala el paquete Flask-JWT-Extended.
    Configura Flask para usar Flask-JWT-Extended.
    Agrega un endpoint de autenticación para generar tokens JWT.
    Protege la ruta /api usando el decorador @jwt_required().
    Prueba la implementación obteniendo un token JWT y accediendo a la ruta protegida con el token.

##### Documentación

    https://flask-jwt-extended.readthedocs.io/en/stable/

#### Referencias

    Autenticación mediante Json Web Token (JWT) en Flask 🤓 con Flask RestFul + MySQL
    JSON Web Token, REST API con Flask
    Construir API REST paso a paso con Django Rest Framework

##### Paquete para configurar fecha con la zona horaria

    https://pypi.org/project/pytz/
