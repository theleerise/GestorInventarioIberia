from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Users(db.Model):
    
    __tablename__ = 'users'
    
    # Definición del modelo
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    locked   = db.Column(db.String(2), nullable=False)
    roles    = db.Column(db.String(20), nullable=False, default="USER")

    def __init__(self, username, password, locked, roles="USER"):
        self.username = username
        self.password = password	
        self.locked   = locked
        self.roles    = roles
        
    # Método para convertir la instancia a un diccionario
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "locked":   self.locked,
            "roles":    self.roles
        }

class UsersVARGS:
    def __init__(self):
        self.username = "Usuario"
        self.password = "Contraseña"
        self.locked   = "Activo/Inactivo"
        self.roles    = "Rol"
