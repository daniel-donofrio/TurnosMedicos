from flask import Blueprint, jsonify, request
from modelos.pacientes import agregar_paciente, obtener_pacientes, obtener_paciente_por_id, actualizar_paciente_por_id, eliminar_paciente_por_id

pacientes_bp = Blueprint('pacientes_bp', __name__)

@pacientes_bp.route('/pacientes', methods=['GET'])
def obtener_lista_pacientes():
    paciente = obtener_pacientes()
    if len(paciente) > 0:
        return jsonify(paciente), 200
    else:
        return jsonify({'error': 'No hay pacientes cargados'}), 404

@pacientes_bp.route('/pacientes/<int:id>', methods=['GET'])
def buscar_paciente_por_id(id):
    paciente = obtener_paciente_por_id(id)
    if paciente:
        return jsonify(paciente), 200
    else:
	    return jsonify({'error': 'Paciente no encontrado'}), 404

@pacientes_bp.route('/pacientes', methods=['POST'])
def crear_paciente():
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'email' in nuevo and 'direccion_calle' in nuevo and 'direccion_numero' in nuevo:
            nuevo_paciente = agregar_paciente(nuevo['dni'], nuevo['nombre'], nuevo['apellido'], nuevo['telefono'], nuevo['email'], nuevo['direccion_calle'], nuevo['direccion_numero'])
            return jsonify(nuevo_paciente), 201
        else:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400
    else:
        return jsonify({'error': 'La solicitud no contiene JSON'}), 400

@pacientes_bp.route('/pacientes/<int:id>', methods=['PUT'])
def actualizar_paciente(id):
    if request.is_json:
       actual = request.get_json()
       if 'dni' in actual and 'nombre' in actual and 'apellido' in actual and 'telefono' in actual and 'email' in actual and 'direccion_calle' in actual and 'direccion_numero' in actual:
           paciente = actualizar_paciente_por_id(id, actual['dni'], actual['nombre'], actual['apellido'], actual['telefono'], actual['email'], actual['direccion_calle'], actual['direccion_numero'])
           if paciente:
               return jsonify(paciente), 200
           else:
               return jsonify({'error': 'Paciente no encontrado'}), 404
       else:
           return jsonify({'error': 'Faltan datos obligatorios'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400
    
@pacientes_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def eliminar_paciente(id):
    paciente = eliminar_paciente_por_id(id)
    if paciente:
        return jsonify({'mensaje': 'El paciente ha sido eliminado'}), 200
    else:
        return jsonify({'error': 'El paciente no pudo ser eliminado'}), 404
