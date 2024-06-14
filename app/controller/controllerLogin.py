
from flask import session

# Para redimensionar la imagen de perfil
from PIL import Image
import os
import uuid  # Modulo de python para crear un string

from config.bd import *
from werkzeug.security import generate_password_hash, check_password_hash


def procesar_insert_userBD(user, email_user, tlf_user, pass_user, process_foto_name):
    try:
        # Generación de la contraseña cifrada
        nueva_password = generate_password_hash(pass_user, method='scrypt')

        # Conexión a la base de datos
        with connectionBD() as conexion_MySQLdb, conexion_MySQLdb.cursor(dictionary=True) as cursor:
            # Comprobar si ya existe una cuenta con el mismo correo electrónico
            cursor.execute(
                "SELECT * FROM tbl_users WHERE email_user = %s", (email_user,))
            result = cursor.fetchone()

            if result is not None:
                return 'Ya existe una cuenta con este correo electrónico.'

            # Insertar una nueva cuenta en la tabla de cuentas
            sql = "INSERT INTO tbl_users (user, email_user, tlf_user, pass_user, foto_user) VALUES (%s, %s, %s, %s, %s)"
            valores = (user, email_user, tlf_user,
                       nueva_password, process_foto_name)
            cursor.execute(sql, valores)
            conexion_MySQLdb.commit()

            resultado_insert = cursor.rowcount

        # Retornar el resultado de la inserción
        return resultado_insert

    except Exception as e:
        return f'Se produjo un error al insertar la cuenta en la base de datos: {str(e)}'


def verificar_password(password_plano, password_hash):
    return check_password_hash(password_hash, password_plano)


def validad_loginBD(email_user, pass_user):
    # Usando 'BINARY' para hacer una comparación sensible entre mayúsculas y minúsculas en MySQL
    with connectionBD() as conexion_MySQLdb, conexion_MySQLdb.cursor(dictionary=True) as cursor:
        cursor.execute(
            "SELECT * FROM tbl_users WHERE BINARY email_user = %s", [email_user])
        usuario = cursor.fetchone()

    if usuario:
        if check_password_hash(usuario['pass_user'], pass_user):
            session['conectado'] = True
            session['id_user'] = usuario['id_user']
            session['user'] = usuario['user']
            session['email_user'] = usuario['email_user']
            session['foto_user'] = usuario['foto_user']

            update_status_user(usuario['id_user'], 1)
            return 1
        else:
            return 0


# Actualizar el status del usuario que se ha conectado
def update_status_user(id_user, status):
    try:
        with connectionBD() as conexion_MySQLdb, conexion_MySQLdb.cursor(dictionary=True) as mycursor:
            mycursor.execute("""
                UPDATE tbl_users
                SET
                    online = %s
                WHERE id_user = %s
                """, (status, id_user))
            conexion_MySQLdb.commit()
            return mycursor.rowcount
    except Exception as e:
        return f'Se produjo un error al insertar la cuenta en la base de datos: {str(e)}'


def procesar_foto_perfil(archivo):
    try:
        extension = os.path.splitext(archivo.filename)[1]

        foto_perfil = str(uuid.uuid4().hex) + extension

        # Construir la ruta completa de subida del archivo
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(basepath, '../static', 'fotos_users')

        # Validar si existe la ruta y crearla si no existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Construir la ruta completa de subida del archivo
        upload_path = os.path.join(upload_dir, foto_perfil)

        # Guardar la imagen original
        archivo.save(upload_path)

        # Abrir la imagen con Pillow
        img = Image.open(upload_path)

        # Redimensionar la imagen manteniendo la proporción
        img.thumbnail((150, 150))

        # Crear una nueva imagen de 150x150 con fondo blanco
        fondo_blanco = Image.new('RGB', (150, 150), (255, 255, 255))

        # Calcular las coordenadas para centrar la imagen original en el fondo blanco
        offset_x = (fondo_blanco.width - img.width) // 2
        offset_y = (fondo_blanco.height - img.height) // 2

        # Superponer la imagen original en el fondo blanco
        fondo_blanco.paste(img, (offset_x, offset_y))

        # Guardar la imagen final con fondo blanco y tamaño mínimo
        fondo_blanco.save(upload_path)

        return foto_perfil

    except Exception as e:
        print("Error:", e)
        return False
