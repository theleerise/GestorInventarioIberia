from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

class Consumible(db.Model):
    
    __tablename__ = 'consumible'
    
    # Definición del modelo
    id = db.Column(db.Integer, primary_key=True)
    ata = db.Column(db.Integer, nullable=False)
    part_num = db.Column(db.String(128), nullable=False)
    serial_num = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    type_quantity = db.Column(db.String(16), nullable=True)
    expiration = db.Column(db.String(8), nullable=False)
    
    def __init__(self, ata, part_num, serial_num, description, quantity, type_quantity, expiration):
        self.ata = ata
        self.part_num = part_num
        self.serial_num = serial_num
        self.description = description
        self.quantity = quantity
        self.type_quantity = type_quantity
        self.expiration = expiration
    
    def to_dict(self):
        return {
            'id': self.id,
            'ata': self.ata,
            'part_num': self.part_num,
            'serial_num': self.serial_num,
            'description': self.description,
            'quantity': self.quantity,
            'type_quantity': self.type_quantity,
            'expiration': self.expiration
        }
    
class ConsumibleVARGS:
    def __init__(self):
        self.id = "Id"
        self.ata = "ATA"
        self.part_num = "Part Number"
        self.serial_num = "Serial Number"
        self.description = "Description"
        self.quantity = "Quantity"
        self.type_quantity = "Unid."
        self.expiration = "Expiration"
