from flask import Blueprint, jsonify, request
from modelos.agenda_medicos import mostrar_agenda, agregar_dia_y_horario, actualizar_horario_por_id, eliminar_dia_por_id

agenda_bp = Blueprint('agenda_bp', __name__)

@agenda_bp.route('/agenda', methods=['GET'])
def mostrarAgenda():
    agenda = mostrar_agenda()
    if len(agenda) > 0:
        return jsonify(agenda), 200
    else:
        return jsonify({'error': 'No registros en la agenda'}), 404

@agenda_bp.route('/agenda', methods=['POST'])
def agregarDiaYHorario():
    if request.is_json:
        nuevo = request.get_json()
        if 'id_medico' in nuevo and 'dia_numero' in nuevo and 'hora_inicio' in nuevo and 'hora_fin' in nuevo:
            resultado = agregar_dia_y_horario(nuevo['id_medico'], nuevo['dia_numero'], nuevo['hora_inicio'], nuevo['hora_fin'])
            
            # Verificar si el resultado contiene el mensaje de error
            if 'error' in resultado:
                return jsonify(resultado), 400
            else:
                return jsonify(resultado), 201
        else:
            return jsonify({'error': 'Datos incompletos'}), 400
    else:
        return jsonify({'error': 'No se enviaron datos en formato JSON'}), 400

@agenda_bp.route('/agenda/<int:id>', methods=['PUT'])
def actualizarHorarioPorId(id):
    if request.is_json:
        horario = request.get_json()
        if 'id_medico' in horario and 'dia_numero' in horario and 'hora_inicio' in horario and 'hora_fin' in horario:
            nuevo_horario = actualizar_horario_por_id(horario['id_medico'], horario['dia_numero'], horario['hora_inicio'], horario['hora_fin'])
            if nuevo_horario:
                return jsonify(nuevo_horario), 200
            else:
                return jsonify({'error': 'El dia y horario ya existe'}), 400
        else:
            return jsonify({'error': 'Datos incompletos'}), 400
    else:
        return jsonify({'error': 'No se enviaron datos en formato JSON'}), 400
    
@agenda_bp.route('/agenda/<int:id>/<int:dia>', methods=['DELETE'])
def eliminar_dia_id(id, dia):
    dia = eliminar_dia_por_id(id, dia)
    if dia:
        return jsonify({'mensaje': 'El dia de atencion ha sido eliminado'}), 200
    else:
        return jsonify({'error': 'El dia de atencion no pudo ser eliminado'}), 404