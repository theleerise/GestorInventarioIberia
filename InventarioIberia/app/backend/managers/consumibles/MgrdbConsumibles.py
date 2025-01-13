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
    
    def update(self, record_or_id, **kwargs):
        """
        Actualiza un registro existente.
        :param record_or_id: Instancia del modelo o ID del registro a actualizar.
        :param kwargs: Campos y valores a actualizar.
        :return: Instancia actualizada o None si no se encontró.
        """
        # Si se pasa una instancia, úsala directamente
        if isinstance(record_or_id, self.model):
            record = record_or_id
        else:
            # Si se pasa un ID, búscalo
            record = self.get_by_id(record_or_id)

        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)  # Asignar atributos dinámicamente
            self.db.session.commit()
            return record
        return None
