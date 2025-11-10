from repo.product_repo import get_product_repo


class ProductService:
    """Lógica de negocio mínima para productos."""

    def __init__(self):
        # factory devuelve la implementación apropiada
        self.repo = get_product_repo()

    def list_products(self):
        return self.repo.list_all()

    def get_product(self, pid):
        return self.repo.get(pid)

    def create_product(self, data):
        return self.repo.create(data)

    def update_product(self, pid, data):
        return self.repo.update(pid, data)

    def delete_product(self, pid):
        return self.repo.delete(pid)
