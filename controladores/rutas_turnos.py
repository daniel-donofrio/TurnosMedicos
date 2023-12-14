from flask import Blueprint, jsonify, request
from modelos.turnos import obtener_turnos_por_id, obtener_turnos, agregar_turno,obtener_turnos_pendientes_por_id
# from modelos.agenda_medicos import mostrar_agenda


turnos_bp = Blueprint('turnos_bp', __name__)

@turnos_bp.route('/turnos/<int:id>', methods=['GET'])
def mostrarTurnos(id):
    turnos = obtener_turnos_por_id(id)
    if turnos:
        return jsonify(turnos), 200
    else:
        return jsonify({'error': 'No hay registros'}), 404
    


@turnos_bp.route('/turnos/pendientes/<int:id>', methods = ['GET'])
def obtener_turnos_pendiente_id(id):
    turnos = obtener_turnos_pendientes_por_id(id)
    if turnos:
        return jsonify(turnos), 200
    else:
        return jsonify({'error': 'No hay turnos pendientes'}), 404

