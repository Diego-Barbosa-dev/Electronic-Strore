from flask import Blueprint, jsonify, request

from services.product_service import ProductService

products_bp = Blueprint('products', __name__)
service = ProductService()


@products_bp.route('/', methods=['GET'])
def list_products():
    """List all products."""
    return jsonify(service.list_products()), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = service.get_product(product_id)
    if not p:
        return jsonify({'error': 'product not found'}), 404
    return jsonify(p), 200


@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json() or {}
    if 'name' not in data:
        return jsonify({'error': 'name is required'}), 400
    p = service.create_product(data)
    return jsonify(p), 201


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json() or {}
    p = service.update_product(product_id, data)
    if not p:
        return jsonify({'error': 'product not found'}), 404
    return jsonify(p), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    ok = service.delete_product(product_id)
    if not ok:
        return jsonify({'error': 'product not found'}), 404
    return ('', 204)
