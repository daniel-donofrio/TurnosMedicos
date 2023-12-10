import requests, csv, os

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

def agregar_dia_y_horario(id_medico, dia_numero, hora_inicio, hora_fin, fecha_actualizacion):       
    agenda.append({
        'id_medico': id_medico,
        'dia_numero': dia_numero,
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
        'fecha_actualizacion': fecha_actualizacion
    })
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
        if medico['dia_numero'] == dia_numero:
            medico['hora_inicio'] = hora_inicio
            medico['hora_fin'] = hora_fin
            medico['fecha_actualizacion'] = fecha_actualizacion
            exportar_datos_a_csv()
            return medico
    return None