import requests, csv, os
from datetime import datetime

turnos = []
ruta_turnos = 'modelos\\turnos.csv'
ruta_agenda = 'modelos\\agendas.csv'

def obtener_turnos_por_id(id):
    for turno in turnos:
        if turno['id_medico'] == id:
            return turno
    return None

def importar_datos_desde_csv():
    global turnos
    turnos = []
    with open(ruta_turnos, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['id_medico'] = int(row['id_medico'])
            row['id_paciente'] = int(row['id_paciente'])
            turnos.append(row)

def inicializar_turnos():
    importar_datos_desde_csv()
    return turnos

        