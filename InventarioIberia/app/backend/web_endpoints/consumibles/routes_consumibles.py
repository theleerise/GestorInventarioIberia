from flask import Blueprint, render_template, request, redirect, url_for, flash
from ....backend.managers.consumibles.MgrdbConsumibles import MgrdbConsumibles
from ....backend.models.consumibles import Consumible, ConsumibleVARGS

bp = Blueprint('consumibles', __name__, url_prefix='/consumibles')

@bp.route('/consumibles_list', methods=['GET'])
def consumibles_list():
    """
    Lista todos los consumibles y los muestra en una tabla.
    """
    mgr = MgrdbConsumibles()
    all_list = mgr.get_all()

    # Convertir cada objeto Consumible a un diccionario usando to_dict()
    consumibles_dict = [consumible.to_dict() for consumible in all_list]

    datadict = consumibles_dict
    
    # Cargar las variables de configuración de la tabla (VARGS)
    vargs = ConsumibleVARGS()
    vargs.table_name = "Lista de Consumibles"
    vargs.table_id = "table_consumibles"
    vargs.search_box = "table_search"
    
    return render_template('wp_consumibles_list.html', 
                           datadict=datadict, 
                           vargs=vargs, 
                           form_url="consumibles.consumible_form", 
                           del_url="consumibles.consumibles_delete")

@bp.route('/consumibles_delete/<string:id>', methods=['POST', 'GET'])
def consumibles_delete(id):
    """
    Elimina un consumible basado en su ID.
    
    :param id: ID del consumible a eliminar.
    :return: Redirige a la lista de consumibles con un mensaje de éxito o error.
    """
    # Inicializar el manager de consumibles
    manager = MgrdbConsumibles()
    
    # Intentar eliminar el registro
    try:
        success = manager.delete(id)
        if success:
            flash('Consumible eliminado con éxito.', 'success')
        else:
            flash('No se pudo encontrar el consumible con el ID proporcionado.', 'error')
    except Exception as e:
        flash(f'Error al eliminar el consumible: {str(e)}', 'error')
    
    # Redirigir a la lista de consumibles
    return redirect(url_for('consumibles.consumibles_list'))

@bp.route("/consumibles_form/<string:id>", methods=["GET", "POST"])
@bp.route('/consumibles_form', defaults={'id': None}, methods=['GET', 'POST'])
def consumible_form(id=None):
    """
    Maneja la creación y edición de registros de consumibles.

    :param id: ID del consumible a editar. Si es None, se creará un nuevo registro.
    :return: Renderiza el formulario para crear/editar consumibles.
    """
    manager = MgrdbConsumibles()

    # Si el ID no viene en la URL, intentar obtenerlo del formulario
    if not id:
        id = request.form.get('id')

    consumible = None
    if id:
        consumible = manager.get_by_id(id)
        if not consumible:
            flash('El consumible no existe.', 'error')
            return redirect(url_for("consumibles.consumibles_list"))

    if request.method == 'POST':
        # Obtener datos del formulario
        ata = request.form.get('ata')
        part_num = request.form.get('part_num')
        serial_num = request.form.get('serial_num')
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        type_quantity = request.form.get('type_quantity')
        expiration = request.form.get('expiration')

        # Validaciones básicas
        if not ata or not part_num or not serial_num or not expiration:
            flash('ATA, Part Number, Serial Number y Expiration son obligatorios.', 'error')
            return render_template('wp_consumibles_form.html', consumible=consumible)

        try:
            quantity = int(quantity) if quantity else None
            ata = int(ata)

            if consumible:
                # Actualizar el consumible existente
                manager.update(
                    consumible,
                    ata=ata,
                    part_num=part_num,
                    serial_num=serial_num,
                    description=description,
                    quantity=quantity,
                    type_quantity=type_quantity,
                    expiration=expiration
                )
                flash('Consumible actualizado con éxito.', 'success')
            else:
                # Crear nuevo consumible
                nuevo_consumible = {
                    'ata': ata,
                    'part_num': part_num,
                    'serial_num': serial_num,
                    'description': description,
                    'quantity': quantity,
                    'type_quantity': type_quantity,
                    'expiration': expiration
                }
                manager.create(**nuevo_consumible)
                flash('Consumible creado con éxito.', 'success')

            # Redirigir a la lista de consumibles
            return redirect(url_for("consumibles.consumibles_list"))

        except ValueError:
            flash('Error en los datos ingresados. Verifique que los campos numéricos sean válidos.', 'error')
            return render_template('wp_consumibles_form.html', consumible=consumible)

    return render_template('wp_consumibles_form.html', consumible=consumible)
