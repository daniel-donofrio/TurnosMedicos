import csv, os
from datetime import datetime
from modelos.medicos import validar_medico_por_id
from modelos.pacientes import paciente_existe
from modelos.agenda_medicos import validar_dia_medico, validar_horario

turnos = []

ruta_turnos = 'modelos\\turnos.csv'

agenda = []
ruta_agenda = 'modelos\\agendas.csv'


def importar_datos_desde_csv():
    global turnos
    turnos = []
    with open(ruta_turnos, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['id_medico'] = int(row['id_medico'])
            row['id_paciente'] = int(row['id_paciente'])
            turnos.append(row)
    
def exportar_datos_a_csv():
    with open(ruta_turnos, mode='w', newline='', encoding='utf8') as csvfile:
        campos_nombres = ['id_medico','id_paciente','hora_turno','fecha_solicitud']
        writer = csv.DictWriter(csvfile, fieldnames=campos_nombres)
        writer.writeheader()
        for turno in turnos:
            writer.writerow(turno)

def inicializar_turnos():
    if os.path.exists(ruta_turnos):
        importar_datos_desde_csv()


def obtener_turnos_por_id(id):
    obtener_turnos= []
    for turno in turnos:
        if turno['id_medico'] == id:
            obtener_turnos.append(turno)
    return obtener_turnos

def obtener_turnos():
    importar_datos_desde_csv()
    return turnos


def obtener_turnos_pendientes_por_id(id_medico):

    dia_actual = datetime.now()
    hora_actual = datetime.now().hour
    
    turnos_pendientes = []
    for turno in turnos:
        fecha_solicitud = datetime.strptime(turno['fecha_solicitud'], '%d/%m/%Y')
        hora_turno = datetime.strptime(turno['hora_turno'], '%H:%M')

        if turno['id_medico'] == id_medico:
            if fecha_solicitud.date() > dia_actual.date() or (fecha_solicitud.date() == dia_actual.date() and str(hora_turno) >= str(hora_actual)):
                turnos_pendientes.append(turno)
                
    return turnos_pendientes

def validar_turno_a_30_dias(fecha_solicitud):
    fecha_hoy = datetime.now()
    fecha_solicitud = datetime.strptime(fecha_solicitud, '%d/%m/%Y')
    diferencia = fecha_solicitud.date() - fecha_hoy.date()
    if 0 <= diferencia.days <= 30:
        return True
    else:
        return False

        
def registrar_turno(id_medico, id_paciente, hora_turno, fecha_solicitud):
    turno = {
        'id_medico': id_medico,
        'id_paciente': id_paciente,
        'hora_turno': hora_turno,
        'fecha_solicitud': fecha_solicitud
    }
    if validar_medico_por_id(id_medico):
        if validar_dia_medico(id_medico, fecha_solicitud):
            if paciente_existe(id_paciente):
                if validar_turno_a_30_dias(fecha_solicitud):
                    if validar_horario(id_medico, hora_turno):
                        if turno_existe(id_medico, hora_turno, fecha_solicitud):
                            turnos.append(turno)
                            exportar_datos_a_csv()
                            return {'mensaje': 'Turno registrado exitosamente'}
                        else:
                            return {'error': 'El turno ya existe'}
                    else:
                        return {'error': 'El turno se encuentra fuera del rango horario disponible'}
                else:
                    return {'error': 'El turno se encuentra fuera del rango de los 30 dias'}
            else:
                return {'error': 'El paciente no se encuentra registrado'}
        else:
            return {'error': 'El medico no atiende en el dia ingresado'}
    else:
        return {'error': 'El medico no se encuentra habilitado'}

def turno_existe(id_medico, hora_turno, fecha_solicitud):
    fecha_solicitud = datetime.strptime(fecha_solicitud, '%d/%m/%Y')
    for turno in turnos:
        if turno['id_medico'] == id_medico and turno['hora_turno'] == hora_turno and turno['fecha_solicitud'] == fecha_solicitud:
            return True
    return False

def eliminar_turno(id_medico, hora_turno, fecha_solicitud):
    for turno in turnos:
        if turno['id_medico'] == int(id_medico) and turno['hora_turno'] == hora_turno and turno['fecha_solicitud'] == fecha_solicitud:
            turnos.remove(turno)
            exportar_datos_a_csv()
            return True
