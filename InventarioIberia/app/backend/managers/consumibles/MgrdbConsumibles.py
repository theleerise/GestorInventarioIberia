from app import db

from app.backend.managers.MgrdbBase import MgrdbBase # Importa la clase base
from app.backend.models.consumibles import Consumible # Importa tu modelo Herramienta

class MgrdbConsumibles(MgrdbBase):
    def __init__(self):
        super().__init__(Consumible)  # Pasa el modelo Herramienta a la clase base

    # Aquí puedes sobreescribir o agregar métodos específicos para Herramientas
    def get_next_id(self):
        """Calcula el siguiente ID disponible para la tabla."""
        max_id = self.db.session.query(self.db.func.max(self.model.id)).scalar()
        return (max_id or 0) + 1
