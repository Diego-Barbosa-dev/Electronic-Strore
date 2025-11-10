# API REST mínima (Flask)

Rápida guía para arrancar la API REST mínima ubicada en `logic/`.

Instalación:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ejecutar:

```bash
# desde la raíz del repositorio
# (opcional) exporta DATABASE_URL para usar la base de datos MariaDB/Mysql
export DATABASE_URL='mysql+pymysql://root@localhost/electronic_store'
python logic/app.py
```

Endpoints:

- GET  /api/health
- GET  /api/products/
- POST /api/products/
- GET  /api/products/<id>
- PUT  /api/products/<id>
- DELETE /api/products/<id>
