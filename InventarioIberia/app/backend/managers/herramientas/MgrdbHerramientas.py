from app import db
from app.backend.models.herramientas import Herramienta  # Importa tu modelo Herramienta
from app.backend.managers.MgrdbBase import MgrdbBase  # Importa la clase base

class MgrdbHerramientas(MgrdbBase):
    def __init__(self):
        super().__init__(Herramienta)  # Pasa el modelo Herramienta a la clase base

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
