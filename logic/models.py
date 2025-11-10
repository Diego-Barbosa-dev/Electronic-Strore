"""Modelos de datos para la aplicación.

Aquí definimos las clases que representan tablas en la base de datos
usando SQLAlchemy. Cada clase contiene los campos (columnas) y un método
`to_dict()` que convierte la instancia a un diccionario serializable.

Notas importantes:
- `password_hash` se almacena pero no se expone en `to_dict()` por razones de seguridad.
"""

from .db import db


# Modelo para productos
class Product(db.Model):
    """Representa la tabla `products`.

    Campos:
    - id: identificador entero, PK.
    - name: nombre del producto (obligatorio).
    - price: precio (opcional).
    - description: descripción larga (opcional).
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        """Devuelve una representación pública del producto.

        Esta representación se usa en las respuestas JSON de la API.
        """
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
        }


# Modelo para usuarios
class User(db.Model):
    """Representa la tabla `users`.

    Campos principales:
    - id: PK
    - name, email: información básica del usuario
    - address, phone: datos opcionales de contacto
    - password_hash: hash seguro de la contraseña (no exponer)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(512), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        """Devuelve la representación pública del usuario.

        IMPORTANTE: no incluimos `password_hash` en la salida para no exponer información sensible.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'phone': self.phone,
        }
