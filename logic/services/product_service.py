"""Servicio de negocio para productos.

Este módulo actúa como capa intermedia entre los controladores HTTP y el
repositorio (persistencia). Encapsula operaciones CRUD simples sobre productos.
"""

from repo.product_repo import get_product_repo


class ProductService:
    """Servicio que delega operaciones al repositorio adecuado.

    Usa la factory `get_product_repo()` que puede devolver una impl. SQL o
    en memoria (fallback). Mantener la lógica aquí facilita añadir reglas de
    negocio en el futuro (validaciones, transformaciones, eventos, etc.).
    """

    def __init__(self):
        # Obtener la implementación del repositorio (SQL o in-memory)
        self.repo = get_product_repo()

    def list_products(self):
        # Devuelve la lista completa de productos (representación pública)
        return self.repo.list_all()

    def get_product(self, pid):
        # Obtiene un producto por id
        return self.repo.get(pid)

    def create_product(self, data):
        # Crea un producto con los campos proporcionados
        return self.repo.create(data)

    def update_product(self, pid, data):
        # Actualiza un producto existente
        return self.repo.update(pid, data)

    def delete_product(self, pid):
        # Elimina un producto por id
        return self.repo.delete(pid)
