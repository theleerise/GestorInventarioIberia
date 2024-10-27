from flask import Blueprint, render_template, jsonify
from ....backend.managers.rotables.MgrdbRotablesRuedas import MgrdbRotablesaRueda
from ....backend.models.rotables import Rueda, RotableVARGS


bp = Blueprint('ruedas', __name__,  url_prefix='/ruedas')

@bp.route('/ruedas_list', methods=['GET'])
def ruedas_list():
    
    mgr = MgrdbRotablesaRueda()
    
    all_list = mgr.get_all()

    # Convertir cada objeto Consumible a un diccionario usando to_dict()
    ruedas_dict = [rueda.to_dict() for rueda in all_list]
    
    datadict = ruedas_dict
    # print(datadict)
    
    # Cargamos la VARGS
    vargs = RotableVARGS()
    vargs.table_name = "Lista de Ruedas"
    vargs.table_id = "table_consumibles"
    vargs.search_box = "table_search"
    
    return render_template('wp_rotables_list.html', datadict=datadict, vargs=vargs, type_rotable_tittle='Ruedas')

@bp.route('/ruedas_delete/<string:id>', methods=['POST'])
def ruedas_delete(id):
    pass

@bp.route("/ruedas_form/<string:id>", methods=["GET", "POST"])
@bp.route('/ruedas_form', methods=['GET', 'POST'])
def ruedas_form(id=None):
    pass