from flask import Blueprint, render_template, request, redirect, url_for, flash
from ....backend.managers.rotables.MgrdbRotablesStock import MgrdbRotablesStock
from ....backend.models.rotables import Stock, RotableVARGS
from app.backend.web_endpoints.auth import login_required, role_required


bp = Blueprint('stocks', __name__, url_prefix='/stocks')

@bp.route('/stocks_list', methods=['GET'])
@login_required
@role_required("USER")
def stocks_list():
    """
    Lista todos los stocks y los muestra en una tabla.
    """
    mgr = MgrdbRotablesStock()
    all_list = mgr.get_all()

    stocks_dict = [stock.to_dict() for stock in all_list]

    vargs = RotableVARGS()
    vargs.table_name = "Lista de Stocks"
    vargs.table_id = "table_stocks"
    vargs.search_box = "search_stocks"

    return render_template(
        'wp_stocks_list.html',
        datadict=stocks_dict,
        vargs=vargs,
        form_url="stocks.stocks_form",
        del_url="stocks.stocks_delete",
        type_rotable_tittle="Stocks"
    )

@bp.route('/stocks_delete/<string:id>', methods=['POST', 'GET'])
@login_required
@role_required("USER")
def stocks_delete(id):
    """
    Elimina un stock basado en su ID.
    """
    manager = MgrdbRotablesStock()

    try:
        success = manager.delete(id)
        if success:
            flash('Stock eliminado con éxito.', 'success')
        else:
            flash('No se pudo encontrar el stock con el ID proporcionado.', 'error')
    except Exception as e:
        flash(f'Error al eliminar el stock: {str(e)}', 'error')

    return redirect(url_for('stocks.stocks_list'))

@bp.route('/stocks_form/<string:id>', methods=['GET', 'POST'])
@bp.route('/stocks_form', methods=['GET', 'POST'])
@login_required
@role_required("USER")
def stocks_form(id=None):
    """
    Maneja la creación y edición de registros de stocks.
    """
    stock = None
    manager = MgrdbRotablesStock()

    if id:
        stock = manager.get_by_id(id)
        if not stock:
            flash('El stock no existe.', 'error')
            return redirect(url_for("stocks.stocks_list"))

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
            return render_template('wp_stocks_form.html', rotable=stock, type_rotable_tittle="Stocks")

        if stock:
            manager.update(
                stock,
                description=description,
                part_num=part_num,
                serial_num=serial_num,
                expiration_date=expiration_date,
                location=location,
                quantity=quantity,
                type_quantity=type_quantity
            )
            flash('Stock actualizado con éxito.', 'success')
        else:
            nuevo_stock = {
                'description': description,
                'part_num': part_num,
                'serial_num': serial_num,
                'expiration_date': expiration_date,
                'location': location,
                'quantity': quantity,
                'type_quantity': type_quantity
            }
            manager.create(**nuevo_stock)
            flash('Stock creado con éxito.', 'success')

        return redirect(url_for("stocks.stocks_list"))

    return render_template('wp_stocks_form.html', rotable=stock, type_rotable_tittle="Stocks")
