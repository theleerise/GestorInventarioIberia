from flask import Blueprint, render_template, jsonify
from ....backend.managers.rotables.MgrdbRotablesStock import MgrdbRotablesStock
from ....backend.models.rotables import Stock, RotableVARGS


bp = Blueprint('stocks', __name__,  url_prefix='/stocks')

@bp.route('/stocks_list', methods=['GET'])
def stocks_list():
    
    mgr = MgrdbRotablesStock()
    
    all_list = mgr.get_all()

    # Convertir cada objeto Consumible a un diccionario usando to_dict()
    stocks_dict = [stock.to_dict() for stock in all_list]
    
    datadict = stocks_dict
    # print(datadict)
    
    # Cargamos la VARGS
    vargs = RotableVARGS()
    vargs.table_name = "Lista de Stocks"
    vargs.table_id = "table_stocks"
    vargs.search_box = "table_search"
    
    return render_template('wp_rotables_list.html', datadict=datadict, vargs=vargs, type_rotable_tittle='Stock')

@bp.route('/stocks_delete/<string:id>', methods=['POST'])
def stocks_delete(id):
    pass

@bp.route("/stocks_form/<string:id>", methods=["GET", "POST"])
@bp.route('/stocks_form', methods=['GET', 'POST'])
def stocks_form(id=None):
    pass