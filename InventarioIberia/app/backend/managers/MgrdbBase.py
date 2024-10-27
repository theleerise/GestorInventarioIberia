class MgrdbBase:
    
    def __init__(self, model):
        self.model = model
        from app import db
        self.db = db

    
    def get_all(self):
        """Obtiene todos los registros del modelo."""
        return self.model.query.all()

    def get_by_id(self, id):
        """Obtiene un registro por su ID."""
        return self.model.query.get(id)
    
    def create(self, **kwargs):
        """Crea un nuevo registro en la base de datos."""
        new_record = self.model(**kwargs)
        self.db.session.add(new_record)
        self.db.session.commit()
        return new_record
    
    def update(self, id, **kwargs):
        """Actualiza un registro existente."""
        record = self.get_by_id(id)
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            self.db.session.commit()
            return record
        return None
    
    def delete(self, id):
        """Elimina un registro por su ID."""
        record = self.get_by_id(id)
        if record:
            self.db.session.delete(record)
            self.db.session.commit()
            return True
        return False
