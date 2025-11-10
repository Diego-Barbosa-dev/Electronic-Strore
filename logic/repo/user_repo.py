"""Repositorio de usuarios con dos implementaciones:

- InMemoryUserRepo: útil para desarrollo y pruebas rápidas sin BD.
- SQLUserRepo: usa SQLAlchemy cuando el modelo `User` está disponible.

La idea es que el servicio use `get_user_repo()` y no se preocupe por la
persistencia concreta.
"""

from typing import Optional

try:
    # Intentamos importar el modelo SQLAlchemy. Si falla, usamos fallback.
    from models import User as UserModel
    from db import db
    USE_SQL = True
except Exception:
    USE_SQL = False


class InMemoryUserRepo:
    """Implementación en memoria del repositorio de usuarios.

    Almacena un diccionario privado con la estructura:
        { id: { 'id': id, 'name': ..., 'email': ..., 'password_hash': ... } }

    Esta implementación devuelve siempre la representación pública (sin password_hash)
    desde los métodos `create`/`update`/`get` según corresponda.
    """
    def __init__(self):
        self._data = {}
        self._next = 1

    def list_all(self):
        # Devuelve copias para evitar que el llamador mutile la estructura interna
        return [dict(u) for u in self._data.values()]

    def get(self, uid: int) -> Optional[dict]:
        return self._data.get(uid)

    def get_by_email(self, email: str) -> Optional[dict]:
        for u in self._data.values():
            if u.get('email') == email:
                return u
        return None

    def create(self, data: dict) -> dict:
        uid = self._next
        self._next += 1
        item = {
            'id': uid,
            'name': data.get('name'),
            'email': data.get('email'),
            'address': data.get('address'),
            'phone': data.get('phone'),
            'password_hash': data.get('password_hash')
        }
        self._data[uid] = item
        # devolver representación pública (sin password_hash)
        return {k: v for k, v in item.items() if k != 'password_hash'}

    def update(self, uid: int, data: dict) -> Optional[dict]:
        if uid not in self._data:
            return None
        item = self._data[uid]
        for k in ('name', 'email', 'address', 'phone', 'password_hash'):
            if k in data:
                item[k] = data[k]
        self._data[uid] = item
        return {k: v for k, v in item.items() if k != 'password_hash'}

    def delete(self, uid: int) -> bool:
        return self._data.pop(uid, None) is not None


class SQLUserRepo:
    """Implementación que utiliza SQLAlchemy y el modelo `User`.

    Devuelve objetos serializables mediante `to_dict()` del modelo.
    """
    def list_all(self):
        rows = UserModel.query.all()
        return [r.to_dict() for r in rows]

    def get(self, uid: int) -> Optional[dict]:
        r = UserModel.query.get(uid)
        return r.to_dict() if r else None

    def get_by_email(self, email: str) -> Optional[dict]:
        r = UserModel.query.filter_by(email=email).first()
        return r.to_dict() if r else None

    def create(self, data: dict) -> dict:
        u = UserModel(
            name=data.get('name'),
            email=data.get('email'),
            address=data.get('address'),
            phone=data.get('phone'),
            password_hash=data.get('password_hash')
        )
        db.session.add(u)
        db.session.commit()
        return u.to_dict()

    def update(self, uid: int, data: dict) -> Optional[dict]:
        u = UserModel.query.get(uid)
        if not u:
            return None
        for k in ('name', 'email', 'address', 'phone', 'password_hash'):
            if k in data:
                setattr(u, k, data[k])
        db.session.commit()
        return u.to_dict()

    def delete(self, uid: int) -> bool:
        u = UserModel.query.get(uid)
        if not u:
            return False
        db.session.delete(u)
        db.session.commit()
        return True


def get_user_repo():
    """Factory que devuelve la implementación adecuada según la disponibilidad de SQLAlchemy."""
    if USE_SQL:
        return SQLUserRepo()
    return InMemoryUserRepo()
