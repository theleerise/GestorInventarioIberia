from app import db

from app.backend.models.rotables import EnvioMAD # Importa tu modelo Herramienta
from app.backend.managers.MgrdbBase import MgrdbBase # Importa la clase base

class MgrdbRotablesEnvioMAD(MgrdbBase):
    def __init__(self):
        super().__init__(EnvioMAD)  # Pasa el modelo Herramienta a la clase base

    # Aquí puedes sobreescribir o agregar métodos específicos para Herramientas
