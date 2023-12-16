import csv, os
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


def agregar_dia_y_horario(id_medico, dia_numero, hora_inicio, hora_fin):
    fecha_actualizacion = datetime.now().strftime('%d-%m-%Y')
    nuevo_dia_horario = {
        'id_medico': id_medico,
        'dia_numero': dia_numero,
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
        'fecha_actualizacion': fecha_actualizacion
    }

    for dia_horario in agenda:
        if dia_horario['id_medico'] == nuevo_dia_horario['id_medico'] and dia_horario['dia_numero'] == nuevo_dia_horario['dia_numero']:
            horario_inicio = datetime.strptime(dia_horario['hora_inicio'], '%H:%M').time()
            horario_fin = datetime.strptime(dia_horario['hora_fin'], '%H:%M').time()
            nueva_hora_inicio = datetime.strptime(str(hora_inicio), '%H:%M').time()
            nueva_hora_fin = datetime.strptime(str(hora_fin), '%H:%M').time()
            if (nueva_hora_inicio >= horario_inicio and nueva_hora_inicio <=  horario_fin) or (nueva_hora_fin >= horario_inicio and nueva_hora_fin <=  horario_fin):
                return {'error': 'El horario ingresado se encuentra dentro de un rango horario existente'}

    agenda.append(nuevo_dia_horario)
    exportar_datos_a_csv()
    return agenda[-1]
 

def mostrar_agenda_por_id(id_medico):
    for medico in agenda:
        if medico['id_medico'] == id_medico:
            return medico
    return None

def actualizar_horario_por_id(id_medico, dia_numero, hora_inicio, hora_fin):
    mostrar_agenda_por_id(id_medico)
    fecha_hoy = datetime.now().strftime('%d-%m-%Y')
    for medico in agenda:
        if  medico['dia_numero'] == dia_numero:
            medico['id_medico'] = id_medico
            medico['dia_numero'] = dia_numero
            medico['hora_inicio'] = hora_inicio
            medico['hora_fin'] = hora_fin
            medico['fecha_actualizacion'] = fecha_hoy
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

def validar_dia_medico(id_medico, fecha_solicitud):
    fecha_numero = datetime.strptime(fecha_solicitud, '%d/%m/%Y')
    fecha_numero = fecha_numero.strftime('%w')
    for medico in agenda:
        if medico['id_medico'] == id_medico:
            if medico['dia_numero'] == int(fecha_numero):
                return True
    return False
        
def validar_horario(id_medico, hora_turno):
    for medico in agenda:
        if medico['id_medico'] == id_medico:
            hora_a_comparar = hora_turno
            hora_inicio = medico['hora_inicio']
            hora_fin = medico['hora_fin']
            hora_a_comparar = datetime.strptime(str(hora_a_comparar), '%H:%M').time()
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            hora_fin = datetime.strptime(hora_fin, '%H:%M').time()
            if hora_inicio <= hora_a_comparar <= hora_fin:	
                return True
    return False
