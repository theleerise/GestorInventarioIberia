from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

# Clase base abstracta que contiene los campos comunes
class BaseModel(db.Model):
    __abstract__ = True  # Esto indica que esta clase no debe crearse como tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128), nullable=True)
    part_num = db.Column(db.String(128), nullable=False)
    serial_num = db.Column(db.String(32), nullable=False)
    expiration_date = db.Column(db.String(16), nullable=False)
    location = db.Column(db.String(8), nullable=False)
    quantity = db.Column(db.String(8), nullable=True)
    type_quantity = db.Column(db.String(16), nullable=True)
    
    def __init__(self, description, part_num, serial_num, expiration_date, location, quantity, type_quantity):
        self.description = description
        self.part_num = part_num
        self.serial_num = serial_num
        self.expiration_date = expiration_date
        self.location = location
        self.quantity = quantity
        self.type_quantity = type_quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'part_num': self.part_num,
            'serial_num': self.serial_num,
            'expiration': self.expiration_date,
            'location': self.location,
            'quantity': self.quantity,
            'type_quantity': self.type_quantity,
        }

# Modelo Rueda heredando de la clase base
class Rueda(BaseModel):
    __tablename__ = 'ruedas'  # Nombre de la tabla en la base de datos

# Modelo Stock heredando de la clase base
class Stock(BaseModel):
    __tablename__ = 'stocks'  # Nombre de la tabla en la base de datos

# Modelo EnvioMAD heredando de la clase base
class EnvioMAD(BaseModel):
    __tablename__ = 'envios_mad'  # Nombre de la tabla en la base de datos


class RotableVARGS:
    def __init__(self):
        self.id = "Id"
        self.description = "Description"
        self.part_num = "Part Number"
        self.serial_num = "Serial Number"
        self.expiration = "Expiration Date"
        self.location = "Location"
        self.quantity = "Quantity"
        self.type_quantity = "Unid."


# class Rueda(db.Model):
#     # Definición del modelo
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     description: Mapped[str] = mapped_column(String(128), nullable=True)
#     part_num: Mapped[str] = mapped_column(String(128), nullable=False)
#     serial_num: Mapped[str] = mapped_column(String(32), nullable=False)
#     expiration_date: Mapped[str] = mapped_column(String(16), nullable=False)
#     location: Mapped[str] = mapped_column(String(8), nullable=False)
#     quantity: Mapped[str] = mapped_column(String(8), nullable=True)
    
# class Stock(db.Model):
#     # Definición del modelo
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     description: Mapped[str] = mapped_column(String(128), nullable=True)
#     part_num: Mapped[str] = mapped_column(String(128), nullable=False)
#     serial_num: Mapped[str] = mapped_column(String(32), nullable=False)
#     expiration_date: Mapped[str] = mapped_column(String(16), nullable=False)
#     location: Mapped[str] = mapped_column(String(8), nullable=False)
#     quantity: Mapped[str] = mapped_column(String(8), nullable=True)

# class EnvioMAD(db.Model):
#     # Definición del modelo
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     description: Mapped[str] = mapped_column(String(128), nullable=True)
#     part_num: Mapped[str] = mapped_column(String(128), nullable=False)
#     serial_num: Mapped[str] = mapped_column(String(32), nullable=False)
#     expiration_date: Mapped[str] = mapped_column(String(16), nullable=False)
#     location: Mapped[str] = mapped_column(String(8), nullable=False)
#     quantity: Mapped[str] = mapped_column(String(8), nullable=True)

