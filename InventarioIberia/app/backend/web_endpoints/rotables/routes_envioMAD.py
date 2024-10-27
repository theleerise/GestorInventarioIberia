from flask import Blueprint, render_template, jsonify
from ....backend.managers.rotables.MgrdbRotablesEnvioMAD import MgrdbRotablesEnvioMAD
from ....backend.models.rotables import EnvioMAD, RotableVARGS


bp = Blueprint('envios_mad', __name__,  url_prefix='/envios_mad')

@bp.route('/envios_mad_list', methods=['GET'])
def envios_mad_list():
    
    mgr = MgrdbRotablesEnvioMAD()
    
    all_list = mgr.get_all()

    # Convertir cada objeto Consumible a un diccionario usando to_dict()
    envios_mad_dict = [envio_mad.to_dict() for envio_mad in all_list]
    
    datadict = envios_mad_dict
    # print(datadict)
    
    # Cargamos la VARGS
    vargs = RotableVARGS()
    vargs.table_name = "Lista de Envios MAD"
    vargs.table_id = "table_envios_mad"
    vargs.search_box = "table_search"
    
    return render_template('wp_rotables_list.html', datadict=datadict, vargs=vargs, type_rotable_tittle='Envios MAD')

@bp.route('/ruedas_delete/<string:id>', methods=['POST'])
def envios_mad_delete(id):
    pass

@bp.route("/envios_mad_form/<string:id>", methods=["GET", "POST"])
@bp.route('/envios_mad_form', methods=['GET', 'POST'])
def envios_mad_form(id=None):
    pass