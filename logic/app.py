import os
import sys
from flask import Flask, jsonify

# Make sure the `logic` folder is on the import path so subpackages can be imported
sys.path.append(os.path.dirname(__file__))

def create_app():
    """Factory to create and configure the Flask app."""
    app = Flask(__name__)

    # Config DB (optional)
    from db import db, get_database_uri
    database_uri = get_database_uri()
    if database_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

        # Create tables if needed
        with app.app_context():
            try:
                from models import Product  # noqa: F401
                db.create_all()
            except Exception:
                # table creation failed, continue—repo will fallback to memory
                pass

    # Registrar blueprints de la API.
    # Usamos try/except para permitir que la app arranque incluso si algún módulo
    # falta (útil durante desarrollo o cuando se trabaja con fallback in-memory).
    try:
        from controllers.products import products_bp
        app.register_blueprint(products_bp, url_prefix='/api/products')
    except Exception:
        # Si falla la importación, la app no falla, pero los endpoints de productos no estarán disponibles.
        pass

    # Registrar rutas relacionadas con usuarios (registro / login)
    try:
        from controllers.users import users_bp
        app.register_blueprint(users_bp, url_prefix='/api/users')
    except Exception:
        # Ignorar si no existe; se puede añadir más tarde.
        pass

    # Habilitar CORS (Cross-Origin Resource Sharing) para permitir que el frontend
    # haga peticiones fetch desde otro origen/puerto. Si la dependencia no está
    # instalada, seguimos sin CORS (útil cuando frontend y backend se sirven desde el mismo origen).
    try:
        from flask_cors import CORS
        CORS(app)
    except Exception:
        # No es crítico; solamente afecta a peticiones desde otros orígenes en el navegador.
        pass

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})

    return app


if __name__ == '__main__':
    create_app().run(debug=True)