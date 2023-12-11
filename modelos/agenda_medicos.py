import requests, csv, os
from datetime import datetime

agenda = []
ruta_agenda = 'modelos\\agenda_medicos.csv'

def importar_datos_desde_csv():
    global agenda
    agenda = []
    with open(ruta_agenda, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['id_medico'] = int(row['id_medico'])
            row['dia_numero'] = int(row['dia_numero'])
            agenda.append(row)

def exportar_datos_a_csv():
    with open(ruta_agenda, mode='w', newline='', encoding='utf8') as csvfile:
        campos_nombres = ['id_medico','dia_numero','hora_inicio','hora_fin','fecha_actualizacion']
        writer = csv.DictWriter(csvfile, fieldnames=campos_nombres)
        writer.writeheader()
        for medico in agenda:
            writer.writerow(medico)

def inicializar_agenda():
    global agenda
    if os.path.exists(ruta_agenda):
        importar_datos_desde_csv()

def mostrar_agenda():
    importar_datos_desde_csv()
    agenda_ordenada = sorted(agenda, key=lambda x: (x['id_medico'], x['dia_numero']))
    return agenda_ordenada

from datetime import datetime

def agregar_dia_y_horario(id_medico, dia_numero, hora_inicio, hora_fin, fecha_actualizacion):
    fecha_actualizacion = datetime.now().strftime('%Y/%m/%d')
    nuevo_dia_horario = {
        'id_medico': id_medico,
        'dia_numero': dia_numero,
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
        'fecha_actualizacion': fecha_actualizacion
    }

    # Verificar si la cita ya existe en la agenda
    for dia_horario in agenda:
        fecha = datetime.strptime(dia_horario['fecha_actualizacion'], '%Y/%m/%d')
        fecha_nueva = datetime.strptime(nuevo_dia_horario['fecha_actualizacion'], '%Y/%m/%d')

        if (dia_horario['dia_numero'] == nuevo_dia_horario['dia_numero'] and
                dia_horario['hora_inicio'] == nuevo_dia_horario['hora_inicio'] and
                dia_horario['hora_fin'] == nuevo_dia_horario['hora_fin']):
            return {'error': 'El dia y horario ya existe'}  # Modificación aquí

    agenda.append(nuevo_dia_horario)
    exportar_datos_a_csv()
    return agenda[-1]

def mostrar_agenda_por_id(id_medico):
    for medico in agenda:
        if medico['id_medico'] == id_medico:
            return medico
    return None

def actualizar_horario_por_id(id_medico, dia_numero, hora_inicio, hora_fin, fecha_actualizacion):
    mostrar_agenda_por_id(id_medico)
    for medico in agenda:
        if  medico['dia_numero'] == dia_numero:
            medico['id_medico'] = id_medico
            medico['dia_numero'] = dia_numero
            medico['hora_inicio'] = hora_inicio
            medico['hora_fin'] = hora_fin
            medico['fecha_actualizacion'] = fecha_actualizacion
            exportar_datos_a_csv()
            return medico
    return None

def eliminar_dia_por_id(id_medico, dia_numero):
    for medico in agenda:
        if medico['id_medico'] == id_medico:
            if medico['dia_numero'] == dia_numero:
                agenda.remove(medico)
                exportar_datos_a_csv()
                return True
    return False