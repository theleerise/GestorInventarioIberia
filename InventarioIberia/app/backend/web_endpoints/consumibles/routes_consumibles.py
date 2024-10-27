from flask import Blueprint, render_template, jsonify
from ....backend.managers.consumibles.MgrdbConsumibles import MgrdbConsumibles
from ....backend.models.consumibles import Consumible, ConsumibleVARGS


bp = Blueprint('consumibles', __name__,  url_prefix='/consumibles')

@bp.route('/consumibles_list', methods=['GET'])
def consumibles_list():
    
    mgr = MgrdbConsumibles()
    
    all_list = mgr.get_all()

    # Convertir cada objeto Consumible a un diccionario usando to_dict()
    consumibles_dict = [consumible.to_dict() for consumible in all_list]
    
    datadict = consumibles_dict
    # print(datadict)
    
    # Cargamos la VARGS
    vargs = ConsumibleVARGS()
    vargs.table_name = "Lista de Consumibles"
    vargs.table_id = "table_consumibles"
    vargs.search_box = "table_search"
    
    return render_template('wp_consumibles_list.html', datadict=datadict, vargs=vargs)

@bp.route('/consumibles_delete/<string:id>', methods=['POST'])
def consumibles_delete(id):
    pass

@bp.route("/consumibles_form/<string:id>", methods=["GET", "POST"])
@bp.route('/consumibles_form', methods=['GET', 'POST'])
def consumibles_form(id=None):
    pass