from flask import Blueprint, jsonify, request
from modelos.turnos import obtener_turnos_por_id, obtener_turnos_pendientes_por_id, registrar_turno, eliminar_turno
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

@turnos_bp.route('/turnos', methods=['POST'])
def agregar_turno_post():
    if request.is_json:
        nuevo = request.get_json()
        if 'id_medico' in nuevo and 'id_paciente' in nuevo and 'hora_turno' in nuevo and 'fecha_solicitud' in nuevo:
            resultado = registrar_turno(nuevo['id_medico'], nuevo['id_paciente'], nuevo['hora_turno'], nuevo['fecha_solicitud'])
            if 'error' in resultado:   
                return jsonify(resultado), 400
            else:
                return jsonify(resultado), 201
        else:
            return jsonify({'error': 'Faltan campos obligatorios'}), 400
    else:
        return jsonify({'error': 'No se enviaron datos en formato JSON'}), 400

@turnos_bp.route('/turnos', methods=['DELETE'])
def eliminar_turno_delete():
    if request.is_json:
        turno = request.get_json()
        if 'id_medico' in turno and 'hora_turno' in turno and 'fecha_solicitud' in turno:
            turno_a_eliminar = eliminar_turno(turno['id_medico'], turno['hora_turno'], turno['fecha_solicitud'])
        if turno_a_eliminar:
            return jsonify({'mensaje': 'El turno se ha eliminado correctamente'}), 200
        else:
            return jsonify({'error': 'El turno no existe'}), 404
    else:
        return jsonify({'error': 'No se enviaron datos en formato JSON'}), 400