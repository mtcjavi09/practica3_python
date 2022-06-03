# se referencia a flask
from multiprocessing import connection
from flask import Flask, request
# se referencia psycopg2 para postgre sql
from psycopg2 import connect, extras

# se agrega la variable para la aplicación
app = Flask(__name__)

# se agregan los datos de la base de datos
host = 'ec2-34-230-153-41.compute-1.amazonaws.com'
port = 5432
dbname = 'daads17to2qqm5'
user = 'dstunsoypdpdpn'
password = 'cbb5e68b3caffdb4b5dcfb015ea18957192c8c55560188602e666ddf3e881705'

# se conecta a la base de datos, creando una función para reutilizar esta base de datos en varias funciones


def getConnection():
    connection = connect(host=host, port=port, dbname=dbname,
                         user=user, password=password)
    return connection

# se hace la ruta principal


@app.get('/api/users')
def getUsers():
    return 'getting users'


@app.get('/api/users/1')
def getUser():
    return 'getting user'


@app.post('/api/users')
def createUsers():
    nvoUsuario = request.get_json()
    username = nvoUsuario['username']
    email = nvoUsuario['email']
    contraseña = nvoUsuario['contraseña']
    connection = getConnection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("INSERT INTO users(username, email, contraseña) VALUES(%s, %s, %s) RETURNING *",
                   (username, email, contraseña))
    connection.commit()
    usuarioCreado = cursor.fetchone()
    print(usuarioCreado)
    cursor.close()
    connection.close()
    return 'usuario creado exitosamente'


@app.delete('/api/users/1')
def deleteUser():
    return 'deleting user'


@app.put('/api/users/1')
def updateUsers():
    return 'updating user'


# se inicializa la aplicación
if __name__ == '__main__':
    app.run(debug=True)
