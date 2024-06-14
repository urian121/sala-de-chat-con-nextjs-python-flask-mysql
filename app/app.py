# Importando  flask y algunos paquetes
from flask import Flask, request, jsonify
import requests
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS


# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app


# Configuración del secreto para JWT
# Cambia esta clave secreta por una más segura en producción
app.config['JWT_SECRET_KEY'] = '97110c78ae5105da20fe'

# Inicializar el JWTManager
jwt = JWTManager(app)
# Habilitar CORS para toda la aplicación
CORS(app)


# Creando mi decorador para la ruta Home
@app.route('/welcome', methods=['GET'])
def welcome():
    return jsonify({"message": "¡Bienvenido a la API de Flask!"})


# Endpoint para autenticación y generación de token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Falta JSON en la solicitud"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Aquí deberías verificar el nombre de usuario y la contraseña con tu base de datos
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Nombre de usuario o contraseña incorrectos"}), 401

    # Crear el token de acceso
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Endpoint protegido
@app.route('/ruta-protegida', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Ruta protegida con JWT
@app.route('/api', methods=['GET'])
@jwt_required()
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
