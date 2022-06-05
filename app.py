# se referencia a flask
from asyncio.windows_events import NULL
from multiprocessing import connection
from flask import Flask, request, jsonify, render_template
# se referencia psycopg2 para postgre sql
from psycopg2 import connect, extras
# se referencia cryptography para evitar que la contraseña sea leída
from cryptography.fernet import Fernet
# se referencia a dotenv para leer el archivo .env
from dotenv import load_dotenv
# se referencia a os para leer el contenido del archivo .env
from os import environ

# se lee el archivo .env
load_dotenv()
# se agrega la variable para la aplicación
app = Flask(__name__)
# se genera una clave para cifrar la contraseña
key = Fernet.generate_key()

# se agregan los datos de la base de datos
host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
dbname = environ.get('DB_NAME')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')

# se conecta a la base de datos, creando una función para reutilizar esta base de datos en varias funciones
def getConnection():
    connection = connect(host=host, port=port, dbname=dbname,
                         user=user, password=password)
    return connection

# se agregan las rutas de la api para manejar los datos
@app.get('/api/users')
def getUsers():
    connection = getConnection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("SELECT * FROM users")
    usuarios = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(usuarios)


@app.get('/api/users/<id>')
def getUser(id):
    connection = getConnection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id, ))
    usuario = cursor.fetchone()
    if usuario is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    cursor.close()
    connection.close()
    return jsonify(usuario)


@app.post('/api/users')
def createUsers():
    nvoUsuario = request.get_json()
    username = nvoUsuario['username']
    email = nvoUsuario['email']
    password = Fernet(key).encrypt(bytes(nvoUsuario['password'], 'utf-8'))
    connection = getConnection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s) RETURNING *",
                   (username, email, password))
    connection.commit()
    usuarioCreado = cursor.fetchone()
    print(usuarioCreado)
    cursor.close()
    connection.close()
    return jsonify(usuarioCreado)


@app.delete('/api/users/<id>')
def deleteUser(id):
    connection = getConnection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("DELETE FROM users WHERE id = %s RETURNING *", (id, ))
    usuario = cursor.fetchone()
    connection.commit()
    if usuario is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    cursor.close()
    connection.close()
    return jsonify(usuario)


@app.put('/api/users/<id>')
def updateUsers(id):
    connection = getConnection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    modifyUsuario = request.get_json()
    username = modifyUsuario['username']
    email = modifyUsuario['email']
    password = Fernet(key).encrypt(bytes(modifyUsuario['password'], 'utf-8'))
    cursor.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *",
                   (username, email, password, id))
    usuarioModificado = cursor.fetchone()
    connection.commit()
    if usuarioModificado is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    cursor.close()
    connection.close()
    return jsonify(usuarioModificado)

# se agrega la ruta principal de la aplicación para el frontend
@app.get('/')
def home():
    return render_template('main.html')

# se inicializa la aplicación
if __name__ == '__main__':
    app.run(debug=True)
