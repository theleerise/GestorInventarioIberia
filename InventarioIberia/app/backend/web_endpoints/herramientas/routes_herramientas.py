from flask import Blueprint, render_template, request, redirect, url_for, flash
from ....backend.managers.herramientas.MgrdbHerramientas import MgrdbHerramientas
from ....backend.models.herramientas import Herramienta, HerramientasVARGS

bp = Blueprint('herramientas', __name__, url_prefix='/herramientas')

@bp.route('/herramientas_list', methods=['GET'])
def herramientas_list():
    """
    Lista todas las herramientas y las muestra en una tabla.
    """
    mgr = MgrdbHerramientas()
    all_list = mgr.get_all()

    # Convertir cada objeto Herramienta a un diccionario usando to_dict()
    herramientas_dict = [herramienta.to_dict() for herramienta in all_list]

    datadict = herramientas_dict
    
    # Cargar las variables de configuración de la tabla (VARGS)
    vargs = HerramientasVARGS()
    vargs.table_name = "Lista de Herramientas"
    vargs.table_id = "table_herramientas"
    vargs.search_box = "table_search"
    
    return render_template('wp_herramientas_list.html', 
                           datadict=datadict, 
                           vargs=vargs, 
                           form_url="herramientas.herramientas_form", 
                           del_url="herramientas.herramientas_delete")

@bp.route('/herramientas_delete/<string:id>', methods=['POST', 'GET'])
def herramientas_delete(id):
    """
    Elimina una herramienta basada en su ID.
    
    :param id: ID de la herramienta a eliminar.
    :return: Redirige a la lista de herramientas con un mensaje de éxito o error.
    """
    # Inicializar el manager de herramientas
    manager = MgrdbHerramientas()
    
    # Intentar eliminar el registro
    try:
        success = manager.delete(id)
        if success:
            flash('Herramienta eliminada con éxito.', 'success')
        else:
            flash('No se pudo encontrar la herramienta con el ID proporcionado.', 'error')
    except Exception as e:
        flash(f'Error al eliminar la herramienta: {str(e)}', 'error')
    
    # Redirigir a la lista de herramientas
    return redirect(url_for('herramientas.herramientas_list'))


@bp.route("/herramientas_form/<string:id>", methods=["GET", "POST"])
@bp.route('/herramientas_form', methods=['GET', 'POST'])
def herramientas_form(id=None):
    """
    Maneja la creación y edición de registros de herramientas.

    :param id: ID de la herramienta a editar. Si es None, se creará un nuevo registro.
    :return: Renderiza el formulario para crear/editar herramientas.
    """
    herramienta = None

    # Inicializar el manager de herramientas
    manager = MgrdbHerramientas()

    # Si se pasa un ID, buscamos el registro existente
    if id:
        herramienta = manager.get_by_id(id)
        if not herramienta:
            flash('La herramienta no existe.', 'error')
            return redirect(url_for("herramientas.herramientas_list"))

    if request.method == 'POST':
        # Obtener datos del formulario
        description = request.form.get('description')
        part_num = request.form.get('part_num')
        serial_num = request.form.get('serial_num')
        expiration_date = request.form.get('expiration_date')
        location = request.form.get('location')
        quantity = request.form.get('quantity')
        type_quantity = request.form.get('type_quantity')
        obs = request.form.get('obs')
        company = request.form.get('company')

        # Validaciones básicas
        if not part_num or not serial_num or not expiration_date or not location or not company:
            flash('Part Number, Serial Number, Expiration Date, Location y Company son obligatorios.', 'error')
            return render_template('wp_herramientas_form.html', herramienta=herramienta)

        # Crear o actualizar el objeto Herramienta
        if herramienta:
            # Actualizar utilizando el método actualizado del manager
            manager.update(
                herramienta,
                description=description,
                part_num=part_num,
                serial_num=serial_num,
                expiration_date=expiration_date,
                location=location,
                quantity=int(quantity) if quantity else None,
                type_quantity=type_quantity,
                obs=obs,
                company=company,
            )
            flash('Herramienta actualizada con éxito.', 'success')
        else:
            # Crear nuevo
            nueva_herramienta = {
                'description': description,
                'part_num': part_num,
                'serial_num': serial_num,
                'expiration_date': expiration_date,
                'location': location,
                'quantity': int(quantity) if quantity else None,
                'type_quantity': type_quantity,
                'obs': obs,
                'company': company
            }
            manager.create(**nueva_herramienta)
            flash('Herramienta creada con éxito.', 'success')

        # Guardar cambios en la base de datos
        return redirect(url_for("herramientas.herramientas_list"))

    return render_template('wp_herramientas_form.html', herramienta=herramienta)
