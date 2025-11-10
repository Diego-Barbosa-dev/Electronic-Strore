from flask import Blueprint, jsonify, request

from services.product_service import ProductService

# Blueprint para operaciones CRUD sobre productos.
products_bp = Blueprint('products', __name__)
service = ProductService()


@products_bp.route('/', methods=['GET'])
def list_products():
    """Lista todos los productos.

    Devuelve un array JSON con la representación pública de cada producto.
    """
    return jsonify(service.list_products()), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Devuelve un producto por su id o 404 si no existe."""
    p = service.get_product(product_id)
    if not p:
        return jsonify({'error': 'product not found'}), 404
    return jsonify(p), 200


@products_bp.route('/', methods=['POST'])
def create_product():
    """Crea un nuevo producto.

    Se espera un JSON con al menos el campo `name`.
    """
    data = request.get_json() or {}
    if 'name' not in data:
        return jsonify({'error': 'name is required'}), 400
    p = service.create_product(data)
    return jsonify(p), 201


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza un producto existente.

    Se aceptan campos `name`, `price`, `description` en el JSON.
    Devuelve 404 si el producto no existe.
    """
    data = request.get_json() or {}
    p = service.update_product(product_id, data)
    if not p:
        return jsonify({'error': 'product not found'}), 404
    return jsonify(p), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Elimina un producto por id. Retorna 204 en caso de éxito."""
    ok = service.delete_product(product_id)
    if not ok:
        return jsonify({'error': 'product not found'}), 404
    return ('', 204)
