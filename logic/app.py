import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- CONFIGURACIÓN DE FLASK Y CORS ---
app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
config = {
    "host": "localhost",
    "user": "root",
    "password": "root123",  # cambia si tu contraseña es diferente
    "database": "electronic_store"
}

# --- CREACIÓN DE LA BD Y TABLAS ---
def init_db():
    conn = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"]
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS electronic_store;")
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        precio DECIMAL(10,2)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carrito (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        producto_id INT,
        cantidad INT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
        FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Base de datos y tablas listas.")


# --- FUNCIONES CRUD ---
def crear_usuario(nombre, email, password):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
        (nombre, email, password)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"🧑 Usuario '{nombre}' creado correctamente.")


def crear_producto(nombre, precio):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (%s, %s)",
        (nombre, precio)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"📦 Producto '{nombre}' agregado por ${precio}.")


def agregar_al_carrito(email_usuario, nombre_producto, cantidad):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email_usuario,))
    user = cursor.fetchone()
    if not user:
        raise Exception("Usuario no encontrado.")

    cursor.execute("SELECT id FROM productos WHERE nombre = %s", (nombre_producto,))
    prod = cursor.fetchone()
    if not prod:
        raise Exception("Producto no encontrado.")

    cursor.execute(
        "INSERT INTO carrito (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s)",
        (user[0], prod[0], cantidad)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"🛒 {cantidad}x '{nombre_producto}' añadido al carrito de {email_usuario}.")


# --- ENDPOINTS ---
@app.route('/api/users/register', methods=['POST'])
def api_register():
    data = request.get_json()
    nombre = data.get('name')
    email = data.get('email')
    password = data.get('password')
    try:
        crear_usuario(nombre, email, password)
        return jsonify({"message": "Usuario creado correctamente."}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return jsonify({"error": "El correo ya está registrado."}), 400
        return jsonify({"error": "Error al registrar usuario."}), 400


@app.route('/api/users/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, password FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 401
    if user[3] != password:
        return jsonify({"error": "Contraseña incorrecta."}), 401
    return jsonify({
        "user": {
            "id": user[0],
            "nombre": user[1],
            "email": user[2]
        }
    }), 200


# --- MAIN ---
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
