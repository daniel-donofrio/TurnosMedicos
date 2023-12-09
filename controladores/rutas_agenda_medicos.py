from flask import Blueprint, jsonify, request
from modelos.agenda_medicos import mostrar_agenda

agenda_bp = Blueprint('agenda_bp', __name__)

@agenda_bp.route('/agenda', methods=['GET'])
def mostrarAgenda():
    agenda = mostrar_agenda()
    if len(agenda) > 0:
        return jsonify(agenda), 200
    else:
        return jsonify({'message': 'No registros en la agenda'}), 404