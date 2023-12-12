from flask import Blueprint, jsonify, request
from modelos.turnos import obtener_turnos_por_id

turnos_bp = Blueprint('turnos_bp', __name__)

@turnos_bp.route('/turnos/<int:id>', methods=['GET'])
def mostrarTurnos(id):
    turnos = obtener_turnos_por_id(id)
    if turnos:
        return jsonify(turnos), 200
    else:
        return jsonify({'error': 'No hay registros'}), 404



