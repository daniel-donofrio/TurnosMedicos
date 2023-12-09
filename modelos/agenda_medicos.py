import requests, csv, os

agenda = []
ruta_agenda = 'modelos\\agenda_medicos.csv'

def importar_datos_desde_csv():
    global agenda
    agenda = []
    with open(ruta_agenda, newline='', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
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
    return agenda
