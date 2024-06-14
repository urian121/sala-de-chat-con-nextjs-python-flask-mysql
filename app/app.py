# Importando  flask y algunos paquetes
from flask import Flask, request, jsonify
import requests
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

# Importando Swagger UI
from flask_swagger_ui import get_swaggerui_blueprint

# Importando la conexión a la BD MySQL
from config.bd import connectionBD
from controller.controllerLogin import *


# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app


# Configuración del secreto para JWT
# Cambia esta clave secreta por una más segura en producción
app.config['JWT_SECRET_KEY'] = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'

# Inicializar el JWTManager
jwt = JWTManager(app)

# Habilitar CORS para toda la aplicación
CORS(app)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Flask"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Creando mi decorador para la ruta Home
@app.route('/welcome', methods=['GET'])
def welcome():
    return jsonify({"message": "¡Bienvenido a la API de Flask!"})


@app.route('/crear-cuenta-de-usuario',  methods=['POST'])
def crear_cuenta_de_usuario():
    nombre_user = request.json.get('nombre_user', None).strip()
    email_user = request.json.get('email_user', None).strip()
    password_user = request.json.get('password_user', None).strip()
    sexo_user = request.json.get('sexo_user', None).strip()
    foto_user = request.json.get('foto_user', None).strip()
    description_user = request.json.get('description_user', None).strip()

    if (foto_user):
        process_foto_name = procesar_foto_perfil(foto_user)
        if process_foto_name:
            # Se han validado todos los datos, se puede continuar con el procesamiento en la base de datos
            resultado_insert = procesar_insert_userBD(
                nombre_user, email_user, sexo_user, password_user, process_foto_name)

            if resultado_insert == 1:
                return jsonify(
                    {
                        'status': 'OK',
                        'user': nombre_user,
                        'email_user': email_user,
                    })
            else:
                return jsonify({'status': 'ERROR', 'message': 'No se ha podido insertar el usuario'})
        return jsonify({'status': 'ERROR', 'message': 'Error al procesar la imagen'})
    else:
        return jsonify({'status': 'ERROR', 'message': 'Error al procesar la imagen'})


# Endpoint para autenticación y generación de token
@ app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Falta JSON en la solicitud"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Aquí deberías verificar el nombre de usuario y la contraseña con tu base de datos
    if username != 'test' or password != 'password123':
        return jsonify({"msg": "Nombre de usuario o contraseña incorrectos"}), 401

    # Crear el token de acceso
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Endpoint protegido
@ app.route('/ruta-protegida', methods=['GET'])
@ jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Ruta protegida con JWT
@ app.route('/api', methods=['GET'])
@ jwt_required()
def api():
    URL_API = 'https://jsonplaceholder.typicode.com/users/'
    solic_req = requests.get(URL_API)
    data_API = solic_req.json()  # Este método es conveniente cuando la API devuelve JSON

    if solic_req.status_code == 200:
        return jsonify({'resp': data_API})
    else:
        return jsonify({'resp': 'No hay datos'}), 404


# Arrancando mi Aplicacion
if __name__ == '__main__':
    app.run(debug=True, port=5000)
