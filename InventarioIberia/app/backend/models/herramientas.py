from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Herramienta(db.Model):
    
    __tablename__ = 'herramienta'
    
    # Definición del modelo
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128), nullable=True)
    part_num = db.Column(db.String(128), nullable=False)
    serial_num = db.Column(db.String(32), nullable=False)
    expiration_date = db.Column(db.String(16), nullable=False)
    location = db.Column(db.String(8), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    type_quantity = db.Column(db.String(16), nullable=True)
    obs = db.Column(db.String(32), nullable=True)
    company = db.Column(db.String(32), nullable=False)

    def __init__(self, description, part_num, serial_num, expiration_date, location, quantity, type_quantity, obs, company):
        self.description = description
        self.part_num = part_num
        self.serial_num = serial_num
        self.expiration_date = expiration_date
        self.location = location
        self.quantity = quantity
        self.type_quantity = type_quantity
        self.obs = obs
        self.company = company
    
    # Método para convertir la instancia a un diccionario
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'part_num': self.part_num,
            'serial_num': self.serial_num,
            'expiration_date': self.expiration_date,
            'location': self.location,
            'quantity': self.quantity,
            'type_quantity': self.type_quantity,
            'obs': self.obs,
            'company': self.company
        }

class HerramientasVARGS:
    def __init__(self):
        self.id = "Id"
        self.description = "Description"
        self.part_num = "Part Num"
        self.serial_num = "Serial Num"
        self.expiration_date = "Expiration"
        self.location = "Location"
        self.quantity = "Quantity"
        self.type_quantity = "Unid."
        self.obs = "Observaciones."
        self.company = "Company"
        