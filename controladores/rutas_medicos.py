from flask import Blueprint, jsonify, request
from modelos.medicos import obtener_medicos, obtener_medico_por_id, agregar_medico, actualizar_medico_por_id, deshabilitar_habilitar_medico, eliminar_medico_por_id

medicos_bp = Blueprint('medicos_bp', __name__)

@medicos_bp.route('/medicos', methods=['GET'])
def obtener_lista_medicos():
    medico = obtener_medicos()
    if len(medico) > 0:
        return jsonify(medico), 200
    else:
        return jsonify({'error': 'No hay medicos cargados'}), 404

@medicos_bp.route('/medicos/<int:id>', methods=['GET'])
def buscar_medico_id(id):
    medico = obtener_medico_por_id(id)
    if medico:
        return jsonify(medico), 200
    else:
        return jsonify({'error': 'Medico no encontrado'}), 404

@medicos_bp.route('/medicos', methods=['POST'])
def nuevo_medico():
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'matricula' in nuevo and 'telefono' in nuevo and 'email' in nuevo and 'habilitado':
            nuevo_medico = agregar_medico(nuevo['dni'], nuevo['nombre'], nuevo['apellido'], nuevo['matricula'], nuevo['telefono'], nuevo['email'], nuevo['habilitado'])
            return jsonify(nuevo_medico), 201
        else:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400

@medicos_bp.route('/medicos/<int:id>', methods=['PUT'])
def actualizar_medico(id):
    if request.is_json:
        actual = request.get_json()
        if 'dni' in actual and 'nombre' in actual and 'apellido' in actual and 'matricula' in actual and 'telefono' in actual and 'email' in actual and 'habilitado':
            medico = actualizar_medico_por_id(id, actual['dni'], actual['nombre'], actual['apellido'], actual['matricula'], actual['telefono'], actual['email'], actual['habilitado'])
            if medico:
                return jsonify(medico), 200
            else:
                return jsonify({'error': 'Medico no encontrado'}), 404
        else:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400

# INCOMPLETO
@medicos_bp.route('/medicos/deshabilitar/<int:id>', methods=['PUT'])
def deshabilitar_medico(id):
    medico = deshabilitar_habilitar_medico(id)
    if medico == False:
        return jsonify({'mensaje': 'El medico ha sido deshabilitado'}), 200
    else:
        return jsonify({'mensaje': 'El medico ha sido habilitado'}), 404
        
# Agregamos la opcion de eliminar medico por si el profecional deja de trabajar en la clinica
@medicos_bp.route('/medicos/<int:id>', methods=['DELETE'])
def eliminar_medico(id):
    medico = eliminar_medico_por_id(id)
    if medico:
        return jsonify({'mensaje': 'El medico ha sido eliminado'}), 200
    else:
        return jsonify({'error': 'Medico no encontrado'}), 404