"""Repositorio de productos con soporte dual: SQL (SQLAlchemy) o in-memory fallback.

Este módulo detecta si hay un modelo `Product` y `db` disponibles y, si
es así, usa la implementación SQL. Si no, cae a un repo en memoria.
"""

from typing import Optional

# Intentamos usar la implementación SQL si los módulos están disponibles.
try:
    from models import Product as ProductModel
    from db import db
    USE_SQL = True
except Exception:
    # Si falla la importación (por ejemplo, al ejecutar pruebas o sin DB), usamos el repo en memoria
    USE_SQL = False


class InMemoryRepo:
    """Repositorio simple en memoria para productos.

    Útil para pruebas o cuando la base de datos no está disponible.
    """
    def __init__(self):
        self._data = {}
        self._next = 1

    def list_all(self):
        # Devuelve la lista de productos almacenados
        return list(self._data.values())

    def get(self, pid: int) -> Optional[dict]:
        # Obtiene un producto por id (o None)
        return self._data.get(pid)

    def create(self, data: dict) -> dict:
        # Inserta un nuevo producto y asigna un id incremental
        pid = self._next
        self._next += 1
        item = {
            'id': pid,
            'name': data.get('name'),
            'price': data.get('price'),
            'description': data.get('description')
        }
        self._data[pid] = item
        return item

    def update(self, pid: int, data: dict) -> Optional[dict]:
        # Actualiza campos permitidos si el producto existe
        if pid not in self._data:
            return None
        item = self._data[pid]
        for k in ('name', 'price', 'description'):
            if k in data:
                item[k] = data[k]
        self._data[pid] = item
        return item

    def delete(self, pid: int) -> bool:
        # Elimina el producto; devuelve True si existía
        return self._data.pop(pid, None) is not None


class SQLProductRepo:
    """Repositorio que usa SQLAlchemy y el modelo Product.

    Cada método consulta el modelo y devuelve diccionarios serializables
    mediante `to_dict()` del modelo.
    """
    def list_all(self):
        rows = ProductModel.query.all()
        return [r.to_dict() for r in rows]

    def get(self, pid: int) -> Optional[dict]:
        r = ProductModel.query.get(pid)
        return r.to_dict() if r else None

    def create(self, data: dict) -> dict:
        p = ProductModel(
            name=data.get('name'),
            price=data.get('price'),
            description=data.get('description')
        )
        db.session.add(p)
        db.session.commit()
        return p.to_dict()

    def update(self, pid: int, data: dict) -> Optional[dict]:
        p = ProductModel.query.get(pid)
        if not p:
            return None
        for k in ('name', 'price', 'description'):
            if k in data:
                setattr(p, k, data[k])
        db.session.commit()
        return p.to_dict()

    def delete(self, pid: int) -> bool:
        p = ProductModel.query.get(pid)
        if not p:
            return False
        db.session.delete(p)
        db.session.commit()
        return True


def get_product_repo():
    """Factory: devuelve la implementación apropiada según la configuración."""
    if USE_SQL:
        return SQLProductRepo()
    return InMemoryRepo()
