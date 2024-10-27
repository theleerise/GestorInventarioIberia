from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from jinja2 import ChoiceLoader, FileSystemLoader

import os

# Configuraciones generales de la base de datos y la app
db_uri = 'sqlite:///database_app.db'  # URI de la base de datos SQLite
secret_key = 'dev'  # Clave secreta de desarrollo

# Se utiliza para realizar consultas utilizando ORM con Flask-SQLAlchemy
db = SQLAlchemy()

# Se utiliza para generar consultas con SQL nativo utilizando SQLAlchemy
engine = create_engine(db_uri)

# Definimos la ruta base del proyecto
base_dir = os.path.abspath(os.path.dirname(__file__))

# Definimos los directorios de archivos estáticos, plantillas y macros
templates_dir = os.path.join(base_dir, 'frontend', 'templates')
static_dir = os.path.join(base_dir, 'frontend', 'static')
macros_dir = os.path.join(base_dir, 'frontend', 'macros')  # Directorio de macros

def create_app():
    """
    Función encargada de generar la aplicación junto con
    la configuración necesaria.
    """

    # Creamos la aplicación Flask y definimos las carpetas
    app = Flask(__name__,
                template_folder=templates_dir,
                static_folder=static_dir)

    # Configuración de la aplicación
    app.config.from_mapping(
        DEBUG=True,  # Activar modo depuración
        SECRET_KEY=secret_key,  # Clave secreta para sesiones
        SQLALCHEMY_DATABASE_URI=db_uri,  # URI de la base de datos
        SQLALCHEMY_TRACK_MODIFICATIONS=False  # Desactivar seguimiento de modificaciones
    )
    
    # Inicializamos la base de datos con la aplicación
    db.init_app(app)

    # Configurar cargadores de Jinja2 para plantillas y macros
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(templates_dir),  # Directorio de plantillas
        FileSystemLoader(macros_dir)      # Directorio de macros
    ])

    # Importar los modelos explícitamente antes de crear las tablas
    with app.app_context():
        """Cuando queremos agregar nuevas tablas es necesario importar sus modelos
        aqui para que el constructor tome en cuenta los modelos"""
        from app.backend.models.consumibles import Consumible  # Importa el modelo aquí
        from app.backend.models.herramientas import Herramienta
        from app.backend.models.rotables import Rueda, Stock, EnvioMAD
        db.create_all()  # Crear las tablas

    # Importar los Blueprints después de inicializar la base de datos portable (db)
    from app.backend.web_endpoints.consumibles import routes_consumibles
    from app.backend.web_endpoints.herramientas import routes_herramientas
    from app.backend.web_endpoints.rotables import routes_ruedas, routes_stock, routes_envioMAD
    
    app.register_blueprint(routes_consumibles.bp)
    app.register_blueprint(routes_herramientas.bp)
    app.register_blueprint(routes_ruedas.bp)
    app.register_blueprint(routes_stock.bp)
    app.register_blueprint(routes_envioMAD.bp)

    # Definición de la ruta principal
    @app.route('/')
    def index():
        return render_template("index.html")
    
    return app
