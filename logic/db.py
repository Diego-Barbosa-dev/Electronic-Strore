import os
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance to be initialised by the app factory
db = SQLAlchemy()

def get_database_uri():
    """Construye la DATABASE_URI.

    Prioridad:
    - Variable de entorno DATABASE_URL
    - fallback a conexión local MariaDB: mysql+pymysql://root@localhost/electronic_store

    Nota: asumimos credenciales root sin password si no se proporciona DATABASE_URL.
    Cambiar mediante la variable de entorno para entornos reales.
    """
    url = os.environ.get('DATABASE_URL')
    if url:
        return url
    # fallback razonable para desarrollo local
    return 'mysql+pymysql://root@localhost/electronic_store'
