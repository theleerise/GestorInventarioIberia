from flask import Blueprint, render_template, jsonify
from ....backend.managers.herramientas.MgrdbHerramientas import MgrdbHerramientas
from ....backend.models.herramientas import Herramienta, HerramientasVARGS


bp = Blueprint('herramientas', __name__,  url_prefix='/herramientas')

@bp.route('/herramientas_list', methods=['GET'])
def herramientas_list():
    
    mgr = MgrdbHerramientas()
    
    all_list = mgr.get_all()

    # Convertir cada objeto Consumible a un diccionario usando to_dict()
    herramientas_dict = [herramienta.to_dict() for herramienta in all_list]
    
    datadict = herramientas_dict
    # print(datadict)
    
    # Cargamos la VARGS
    vargs = HerramientasVARGS()
    vargs.table_name = "Lista de Herramientas"
    vargs.table_id = "table_herramientas"
    vargs.search_box = "table_search"
    
    return render_template('wp_herramientas_list.html', datadict=datadict, vargs=vargs)

@bp.route('/herramientas_delete/<string:id>', methods=['POST'])
def herramientas_delete(id):
    pass

@bp.route("/herramientas_form/<string:id>", methods=["GET", "POST"])
@bp.route('/herramientas_form', methods=['GET', 'POST'])
def herramientas_form(id=None):
    pass