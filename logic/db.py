import os
from flask_sqlalchemy import SQLAlchemy

# Instancia de SQLAlchemy que será inicializada por la app factory
db = SQLAlchemy()


def get_database_uri():
    """Construye la URI de conexión a la base de datos.

    Prioridad de resolución:
    1. Variable de entorno DATABASE_URL (recomendada para producción).
    2. Valor por defecto para desarrollo local: 'mysql+pymysql://root@localhost/electronic_store'

    ATENCIÓN: el fallback asume usuario `root` sin contraseña — solo válido para entornos
    de desarrollo locales. En producción, exportar `DATABASE_URL` con credenciales seguras,
    por ejemplo: mysql+pymysql://usuario:password@host:3306/electronic_store
    """
    url = os.environ.get('DATABASE_URL')
    if url:
        return url
    # fallback razonable para desarrollo local
    return 'mysql+pymysql://root@localhost/electronic_store'
