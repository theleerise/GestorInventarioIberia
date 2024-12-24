from flask import Blueprint, render_template, request, redirect, url_for, flash
from ....backend.managers.rotables.MgrdbRotablesEnvioMAD import MgrdbRotablesEnvioMAD
from ....backend.models.rotables import EnvioMAD, RotableVARGS

bp = Blueprint('envios_mad', __name__, url_prefix='/envios_mad')

@bp.route('/envios_mad_list', methods=['GET'])
def envios_mad_list():
    """
    Lista todos los envíos a MAD y los muestra en una tabla.
    """
    mgr = MgrdbRotablesEnvioMAD()
    all_list = mgr.get_all()

    envios_mad_dict = [envio_mad.to_dict() for envio_mad in all_list]

    vargs = RotableVARGS()
    vargs.table_name = "Lista de Envios MAD"
    vargs.table_id = "table_envios_mad"
    vargs.search_box = "search_envios_mad"

    return render_template(
        'wp_envios_mad_list.html',
        datadict=envios_mad_dict,
        vargs=vargs,
        form_url="envios_mad.envios_mad_form",
        del_url="envios_mad.envios_mad_delete",
        type_rotable_tittle="Envios MAD"
    )

@bp.route('/envios_mad_delete/<string:id>', methods=['POST', 'GET'])
def envios_mad_delete(id):
    """
    Elimina un envío a MAD basado en su ID.
    """
    manager = MgrdbRotablesEnvioMAD()

    try:
        success = manager.delete(id)
        if success:
            flash('Envío eliminado con éxito.', 'success')
        else:
            flash('No se pudo encontrar el envío con el ID proporcionado.', 'error')
    except Exception as e:
        flash(f'Error al eliminar el envío: {str(e)}', 'error')

    return redirect(url_for('envios_mad.envios_mad_list'))

@bp.route('/envios_mad_form/<string:id>', methods=['GET', 'POST'])
@bp.route('/envios_mad_form', methods=['GET', 'POST'])
def envios_mad_form(id=None):
    """
    Maneja la creación y edición de registros de envíos a MAD.
    """
    envio_mad = None
    manager = MgrdbRotablesEnvioMAD()

    if id:
        envio_mad = manager.get_by_id(id)
        if not envio_mad:
            flash('El envío no existe.', 'error')
            return redirect(url_for("envios_mad.envios_mad_list"))

    if request.method == 'POST':
        description = request.form.get('description')
        part_num = request.form.get('part_num')
        serial_num = request.form.get('serial_num')
        expiration_date = request.form.get('expiration_date')
        location = request.form.get('location')
        quantity = request.form.get('quantity')
        type_quantity = request.form.get('type_quantity')

        if not part_num or not serial_num or not expiration_date or not location:
            flash('Part Number, Serial Number, Expiration Date y Location son obligatorios.', 'error')
            return render_template('wp_envios_mad_form.html', rotable=envio_mad, type_rotable_tittle="Envios MAD")

        if envio_mad:
            manager.update(
                envio_mad,
                description=description,
                part_num=part_num,
                serial_num=serial_num,
                expiration_date=expiration_date,
                location=location,
                quantity=quantity,
                type_quantity=type_quantity
            )
            flash('Envío actualizado con éxito.', 'success')
        else:
            nuevo_envio = {
                'description': description,
                'part_num': part_num,
                'serial_num': serial_num,
                'expiration_date': expiration_date,
                'location': location,
                'quantity': quantity,
                'type_quantity': type_quantity
            }
            manager.create(**nuevo_envio)
            flash('Envío creado con éxito.', 'success')

        return redirect(url_for("envios_mad.envios_mad_list"))

    return render_template('wp_envios_mad_form.html', rotable=envio_mad, type_rotable_tittle="Envios MAD")
