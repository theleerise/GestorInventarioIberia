from app.backend.models.users import Users  
from app.backend.managers.MgrdbBase import MgrdbBase  
from werkzeug.security import check_password_hash

class MgrdbUsers(MgrdbBase):
    def __init__(self):
        super().__init__(Users)  # Pasa el modelo Users a la clase base

    def get_user_by_username(self, username):
        """Obtiene un usuario por su nombre de usuario"""
        return self.db.session.query(self.model).filter_by(username=username).first()

    def is_user_locked(self, username):
        """Verifica si el usuario está bloqueado"""
        user = self.get_user_by_username(username)
        return user and user.locked == "SI"

    def validate_login(self, username, password):
        """
        Valida el login del usuario verificando su contraseña y estado.
        :return: Usuario si es válido, mensaje de error en caso contrario.
        """
        user = self.get_user_by_username(username)

        if not user:
            return None, "Nombre de usuario incorrecto"
        if user.locked == "SI":
            return None, "Usuario bloqueado. Contacte al administrador."
        if not check_password_hash(user.password, password):
            return None, "Contraseña incorrecta"

        return user, None  # Si todo es válido, devuelve el usuario

    def create_user(self, username, password, locked="NO", roles="USER"):
        """
        Crea un nuevo usuario con rol, utilizando el método create() de MgrdbBase.
        """
        return super().create(username=username, password=password, locked=locked, roles=roles)

    def get_user_role(self, username):
        """
        Obtiene el rol del usuario dado su username.
        """
        user = self.get_user_by_username(username)
        return user.roles if user else None
