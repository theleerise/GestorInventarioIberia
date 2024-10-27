from app import db

from app.backend.models.rotables import Rueda # Importa tu modelo Herramienta
from app.backend.managers.MgrdbBase import MgrdbBase # Importa la clase base

class MgrdbRotablesaRueda(MgrdbBase):
    def __init__(self):
        super().__init__(Rueda)  # Pasa el modelo Herramienta a la clase base

    # Aquí puedes sobreescribir o agregar métodos específicos para Herramientas
