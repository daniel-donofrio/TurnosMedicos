from flask import Blueprint, jsonify, request
from modelos.agenda_medicos import mostrar_agenda, agregar_dia_y_horario

agenda_bp = Blueprint('agenda_bp', __name__)

@agenda_bp.route('/agenda', methods=['GET'])
def mostrarAgenda():
    agenda = mostrar_agenda()
    if len(agenda) > 0:
        return jsonify(agenda), 200
    else:
        return jsonify({'message': 'No registros en la agenda'}), 404

@agenda_bp.route('/agenda', methods=['POST'])
def agregarDiaYHorario():
    if request.is_json:
        nuevo = request.get_json()
        if 'id_medico' in nuevo and 'dia_numero' in nuevo and 'hora_inicio' in nuevo and 'hora_fin' in nuevo and 'fecha_actualizacion' in nuevo:
            nueva_agenda = agregar_dia_y_horario(nuevo['id_medico'], nuevo['dia_numero'], nuevo['hora_inicio'], nuevo['hora_fin'], nuevo['fecha_actualizacion'])
            return jsonify(nueva_agenda), 201
        else:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400
    else:
        return jsonify({'error': 'La solicitud no contiene formato JSON'}), 400