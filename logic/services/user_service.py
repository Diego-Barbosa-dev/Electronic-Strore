"""Lógica de negocio para usuarios.

Este servicio encapsula la validación y la interacción con el repositorio
(in-memory o SQL). También gestiona el hashing de contraseñas.
"""

from repo.user_repo import get_user_repo
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    """Servicio de alto nivel para operaciones sobre usuarios.

    Responsabilidades:
    - Validar datos de entrada.
    - Hashear contraseñas antes de persistir.
    - Delegar operaciones CRUD al repositorio.
    - Proveer un método de autenticación que devuelve la representación pública del usuario.
    """

    def __init__(self):
        # Obtiene la implementación del repo (SQL o in-memory)
        self.repo = get_user_repo()

    def create_user(self, data: dict):
        """Crea un usuario nuevo.

        - Verifica que el email no exista ya.
        - Requiere `password` en texto plano; lo convierte a `password_hash`.
        - Devuelve la representación pública del usuario (sin password_hash).
        """
        email = data.get('email')
        if self.repo.get_by_email(email):
            # evitar registros duplicados por email
            raise ValueError('email already registered')

        pwd = data.get('password')
        if not pwd:
            raise ValueError('password is required')

        user_data = {
            'name': data.get('name'),
            'email': email,
            'address': data.get('address'),
            'phone': data.get('phone'),
            # generamos el hash seguro de la contraseña
            'password_hash': generate_password_hash(pwd)
        }

        return self.repo.create(user_data)

    def authenticate(self, email: str, password: str):
        """Autentica un usuario por email y contraseña.

        - Busca el usuario por email.
        - Compara el hash almacenado con la contraseña proporcionada.
        - Si coincide, devuelve la representación pública del usuario.
        """
        u = self.repo.get_by_email(email)
        if not u:
            return None
        pwd_hash = u.get('password_hash')
        if not pwd_hash:
            return None
        if check_password_hash(pwd_hash, password):
            # devolver representación pública (sin password_hash)
            return {k: v for k, v in u.items() if k != 'password_hash'}
        return None

    def get_user(self, uid: int):
        """Obtiene un usuario por id y devuelve su representación pública."""
        u = self.repo.get(uid)
        if not u:
            return None
        return {k: v for k, v in u.items() if k != 'password_hash'}
