import requests, csv, os
from datetime import datetime
from modelos.agenda_medicos import mostrar_agenda_por_id

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

def agregar_turno(id_medico, id_paciente, hora_turno, fecha_solicitud):
    turnos.append({
        'id_medico': id_medico,
        'id_paciente': id_paciente,
        'hora_turno': hora_turno,
        'fecha_solicitud': fecha_solicitud
    })

# id_medico,dia_numero,hora_inicio,hora_fin,fecha_actualizacion     #agenda_medicos
# 2,2,09:00,20:00,10-12-2023

# id_medico,id_paciente,hora_turno,fecha_solicitud      #turnos
# 1,1,08:00,11/12/2023

#fecha_solicitud(turnos) = dia_numero(agenda_medicos)


def obtener_turnos_pendientes_por_id(id_medico):


    # hora_inicio = datetime.strptime(agenda['hora_inicio'], '%H:%M').time()
    # hora_fin = datetime.strptime(agenda['hora_fin'], '%H:%M').time()

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


# def obtener_turnos_pendientes_por_id(id_medico):

#     turnos= obtener_turnos_por_id(id_medico)
#     agenda = mostrar_agenda_por_id(id_medico)

#     if not turnos or not agenda:
#         return None

#     # hora_inicio = datetime.strptime(agenda['hora_inicio'], '%H:%M').time()
#     # hora_fin = datetime.strptime(agenda['hora_fin'], '%H:%M').time()

    
    
#     turnos_pendientes = []
#     for turno in turnos:
#         dia_actual = datetime.now().strftime('%d-%m-%Y')
#         hora_actual = datetime.now().hour
#         fecha_solicitud = datetime.strptime(turno['fecha_solicitud'], '%d/%m/%Y')
#         hora_turno = datetime.strptime(turno['hora_turno'], '%H:%M').time()
#         hora_turno = datetime.strptime(turno['hora_turno'], '%H:%M').time()
#         fecha_numero = fecha_solicitud.strftime('%w')
#         #Para cada turno, se convierte la cadena de fecha en formato día/mes/año a un objeto datetime para facilitar la comparación.
#         if turno['id_medico'] == agenda['id_medico'] and fecha_numero == agenda['dia_numero']:
#             if turno['fecha_solicitud'] > dia_actual:
#                 turnos_pendientes.append(turno)
#             elif turno['fecha_solicitud'] == dia_actual:
#                     if hora_turno >= hora_actual:
#                         turnos_pendientes.append(turno)
#         return turnos_pendientes
#     return False         
                    

            



# def obtener_turnos_pendientes_por_id(id_medico):
#     turnos = obtener_turnos_por_id(id_medico)
#     agenda = mostrar_agenda(id_medico)

#     if not turnos or not agenda:
#         return None  # Manejar casos donde no hay turnos o agenda para el médico

    # hora_inicio = datetime.strptime(agenda['hora_inicio'], '%H:%M').time()
    # hora_fin = datetime.strptime(agenda['hora_fin'], '%H:%M').time()
    # dia_actual = datetime.now()

    # turnos_pendientes = []
    