from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import generate_password_hash
import functools

from app.backend.managers.MgrdbAuth import MgrdbUsers  

bp = Blueprint('auth', __name__, url_prefix='/auth')

mgr_users = MgrdbUsers()  # Instancia del manager

# 📌 REGISTRO DE USUARIOS
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)  # Encripta la contraseña
        
        error = None
        user_exists = mgr_users.get_user_by_username(username)  # Verifica si el usuario ya existe
        
        if not user_exists:
            mgr_users.create(username=username, password=hashed_password, locked="NO", roles="USER")  # Usa MgrdbBase.create()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya está registrado'
        
        flash(error)
        
    return render_template('auth/register.html')

# 📌 LOGIN DE USUARIOS
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user, error = mgr_users.validate_login(username, password)  # Validación de usuario y contraseña

        if error is None:
            session.clear()
            session['username'] = user.username  # Guarda el username en sesión
            session['role'] = user.roles  # Guarda el rol en sesión
            return render_template("index.html")

        flash(error)
    
    return render_template('auth/login.html')


# 📌 CARGA DEL USUARIO LOGUEADO
@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    
    if username is None:
        g.user = None
    else:
        g.user = mgr_users.get_user_by_username(username)  # Obtiene el usuario

# 📌 LOGOUT (CERRAR SESIÓN)
@bp.route('/logout')
def logout():
    session.pop('role', None)
    session.clear()
    return redirect(url_for('auth.login'))  # Redirige al login después de cerrar sesión

############################################################################
###################### Decoradores de Seguridad ############################
############################################################################

# 📌 DECORADOR PARA RESTRINGIR EL ACCESO A PÁGINAS PROTEGIDAS
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# 📌 DECORADOR PARA RESTRINGIR ACCESO SEGÚN ROL (ADMIN SIEMPRE PUEDE ACCEDER)
def role_required(required_role):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            user_role = session.get('role')

            # Permitir acceso si el usuario es ADMIN o si coincide con el rol requerido
            if g.user is None or (user_role != "ADMIN" and user_role != required_role):
                flash("Acceso denegado. No tienes los permisos necesarios.", "danger")
                return redirect(url_for('auth.login'))
            
            return view(**kwargs)
        return wrapped_view
    return decorator


