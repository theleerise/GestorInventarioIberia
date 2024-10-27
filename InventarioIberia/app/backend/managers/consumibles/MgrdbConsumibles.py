from app.backend.managers.MgrdbBase import MgrdbBase # Importa la clase base

class MgrdbConsumibles(MgrdbBase):
    def __init__(self):
        from app.backend.models.consumibles import Consumible # Importa tu modelo Herramienta
        super().__init__(Consumible)  # Pasa el modelo Herramienta a la clase base

    # Aquí puedes sobreescribir o agregar métodos específicos para Herramientas
