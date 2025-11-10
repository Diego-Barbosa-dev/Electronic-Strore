from flask import Blueprint, request, jsonify

from services.user_service import UserService

# Blueprint para rutas relacionadas con usuarios.
# Separar la lógica de enrutamiento (controllers) de la lógica de negocio (services)
users_bp = Blueprint('users', __name__)
service = UserService()


@users_bp.route('/register', methods=['POST'])
def register_user():
    """Endpoint para registrar un nuevo usuario.

    Espera un JSON con al menos: { name, email, password }.
    - Valida la presencia de campos obligatorios.
    - Llama a UserService.create_user() que realiza hashing de contraseña y persiste el usuario.
    - Devuelve 201 con la representación pública del usuario o 400 en caso de error.
    """
    data = request.get_json() or {}
    # Campos obligatorios: name, email, password
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'name, email and password are required'}), 400

    try:
        user = service.create_user(data)
    except ValueError as e:
        # Errores de validación (por ejemplo: email duplicado)
        return jsonify({'error': str(e)}), 400
    # user ya es la representación pública (sin password_hash)
    return jsonify(user), 201


@users_bp.route('/login', methods=['POST'])
def login_user():
    """Endpoint para autenticación.

    Recibe JSON { email, password } y verifica credenciales.
    - Si son válidas devuelve 200 con información del usuario (sin password_hash).
    - Si no son válidas devuelve 401.
    NOTA: Este endpoint no implementa tokens (JWT). Devuelve la info básica para la demo.
    """
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'email and password are required'}), 400

    user = service.authenticate(email, password)
    if not user:
        return jsonify({'error': 'invalid credentials'}), 401

    # Para simplicidad devolvemos el usuario (sin password_hash) y un flag
    return jsonify({'ok': True, 'user': user}), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Devuelve información pública de un usuario por su id.

    Este endpoint puede usarse para mostrar perfiles o para propósitos administrativos.
    """
    u = service.get_user(user_id)
    if not u:
        return jsonify({'error': 'user not found'}), 404
    return jsonify(u), 200
