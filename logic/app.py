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

    # Blueprints
    try:
        from controllers.products import products_bp
        app.register_blueprint(products_bp, url_prefix='/api/products')
    except Exception:
        # If blueprints can't be imported, still start app and surface an error route
        pass

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})

    return app


if __name__ == '__main__':
    create_app().run(debug=True)