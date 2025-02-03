from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..managers.MgrdbAuth import MgrdbUsers
from ..models.users import UsersVARGS
from app.backend.web_endpoints.auth import login_required, role_required
from werkzeug.security import generate_password_hash

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Directorio base
base_dir = "admin_users/"

# 📌 LISTADO DE USUARIOS
@bp.route('/usuarios_list', methods=['GET'])
@login_required
@role_required("ADMIN")
def usuarios_list():
    """
    Lista todos los usuarios y los muestra en una tabla.
    """
    mgr = MgrdbUsers()
    all_list = mgr.get_all()

    # usuarios_dict = [user.to_dict() for user in all_list]

    vargs = UsersVARGS()
    vargs.table_name = "Lista de Usuarios"
    vargs.table_id = "table_usuarios"
    vargs.search_box = "search_usuarios"

    return render_template(
        base_dir+'wp_admin_user_list.html',
        datadict=all_list,
        vargs=vargs,
        form_url="usuarios.usuarios_form",
        del_url="usuarios.usuarios_delete",
        type_user_title="Usuarios"
    )

# 📌 ELIMINAR USUARIO
@bp.route('/usuarios_delete/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required("ADMIN")
def usuarios_delete(id):
    """
    Elimina un usuario basado en su ID.
    """
    manager = MgrdbUsers()

    try:
        success = manager.delete(id)
        if success:
            flash('Usuario eliminado con éxito.', 'success')
        else:
            flash('No se pudo encontrar el usuario con el ID proporcionado.', 'error')
    except Exception as e:
        flash(f'Error al eliminar el usuario: {str(e)}', 'error')

    return redirect(url_for('usuarios.usuarios_list'))

# 📌 FORMULARIO DE CREACIÓN / EDICIÓN DE USUARIOS
@bp.route('/usuarios_form/<int:id>', methods=['GET', 'POST'])
@bp.route('/usuarios_form', methods=['GET', 'POST'])
@login_required
@role_required("ADMIN")
def usuarios_form(id=None):
    """
    Maneja la creación y edición de usuarios.
    """
    usuario = None
    manager = MgrdbUsers()

    if id:
        usuario = manager.get_by_id(id)
        if not usuario:
            flash('El usuario no existe.', 'error')
            return redirect(url_for("usuarios.usuarios_list"))

    if request.method == 'POST':
        username = request.form.get('username')
        request_password = request.form.get('password')
        password = generate_password_hash(request_password) # Encripta la contraseña
        locked = request.form.get('locked', "NO")
        roles = request.form.get('roles', "USER")

        if not username or not password:
            flash('Usuario y contraseña son obligatorios.', 'error')
            return render_template(base_dir+'wp_admin_user_form.html', usuario=usuario, type_user_title="Usuarios")

        if usuario:
            manager.update(
                usuario.id,
                username=username,
                password=password,
                locked=locked,
                roles=roles
            )
            flash('Usuario actualizado con éxito.', 'success')
        else:
            nuevo_usuario = {
                'username': username,
                'password': password,
                'locked': locked,
                'roles': roles
            }
            manager.create(**nuevo_usuario)
            flash('Usuario creado con éxito.', 'success')

        return redirect(url_for("usuarios.usuarios_list"))

    return render_template(base_dir+'wp_admin_user_form.html', usuario=usuario, type_user_title="Usuarios")
