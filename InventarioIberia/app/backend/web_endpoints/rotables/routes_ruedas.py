from flask import Blueprint, render_template, request, redirect, url_for, flash
from ....backend.managers.rotables.MgrdbRotablesRuedas import MgrdbRotablesRueda
from ....backend.models.rotables import Rueda, RotableVARGS

bp = Blueprint('ruedas', __name__, url_prefix='/ruedas')

@bp.route('/ruedas_list', methods=['GET'])
def ruedas_list():
    """
    Lista todas las ruedas y las muestra en una tabla.
    """
    mgr = MgrdbRotablesRueda()
    all_list = mgr.get_all()

    ruedas_dict = [rueda.to_dict() for rueda in all_list]

    vargs = RotableVARGS()
    vargs.table_name = "Lista de Ruedas"
    vargs.table_id = "table_ruedas"
    vargs.search_box = "search_ruedas"

    return render_template(
        'wp_ruedas_list.html',
        datadict=ruedas_dict,
        vargs=vargs,
        form_url="ruedas.ruedas_form",
        del_url="ruedas.ruedas_delete",
        type_rotable_tittle="Ruedas"
    )

@bp.route('/ruedas_delete/<string:id>', methods=['POST', 'GET'])
def ruedas_delete(id):
    """
    Elimina una rueda basada en su ID.
    """
    manager = MgrdbRotablesRueda()

    try:
        success = manager.delete(id)
        if success:
            flash('Rueda eliminada con éxito.', 'success')
        else:
            flash('No se pudo encontrar la rueda con el ID proporcionado.', 'error')
    except Exception as e:
        flash(f'Error al eliminar la rueda: {str(e)}', 'error')

    return redirect(url_for('ruedas.ruedas_list'))

@bp.route('/ruedas_form/<string:id>', methods=['GET', 'POST'])
@bp.route('/ruedas_form', methods=['GET', 'POST'])
def ruedas_form(id=None):
    """
    Maneja la creación y edición de registros de ruedas.
    """
    rueda = None
    manager = MgrdbRotablesRueda()

    if id:
        rueda = manager.get_by_id(id)
        if not rueda:
            flash('La rueda no existe.', 'error')
            return redirect(url_for("ruedas.ruedas_list"))

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
            return render_template('wp_ruedas_form.html', rotable=rueda, type_rotable_tittle="Ruedas")

        if rueda:
            manager.update(
                rueda,
                description=description,
                part_num=part_num,
                serial_num=serial_num,
                expiration_date=expiration_date,
                location=location,
                quantity=quantity,
                type_quantity=type_quantity
            )
            flash('Rueda actualizada con éxito.', 'success')
        else:
            nueva_rueda = {
                'description': description,
                'part_num': part_num,
                'serial_num': serial_num,
                'expiration_date': expiration_date,
                'location': location,
                'quantity': quantity,
                'type_quantity': type_quantity
            }
            manager.create(**nueva_rueda)
            flash('Rueda creada con éxito.', 'success')

        return redirect(url_for("ruedas.ruedas_list"))

    return render_template('wp_ruedas_form.html', rotable=rueda, type_rotable_tittle="Ruedas")
