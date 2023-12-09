import requests, csv, os

medicos = []
id_medico = 1
ruta_medicos ='modelos\\medicos.csv'


def CargarMedicos():
    url = 'https://randomuser.me/api/?results=5&nat=es&password=number,6'
    ruta_medicos = 'modelos\\medicos.csv'
    response = requests.get(url)  # Cambia el número de resultados si quieres más usuarios

    # Verificar si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        data = response.json()  # Obtener los datos en formato JSON
        #print(data)
    # Abrir un archivo CSV en modo escritura
        with open(ruta_medicos, mode='w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            
            # Escribir encabezados en el archivo CSV
            writer.writerow(['id','dni','nombre', 'apellido','matricula','telefono', 'email', 'habilitado'])
            
            # Iterar a través de los resultados y escribir en el archivo CSV
            for index, medico in enumerate( data['results'], start=1):
                medico_id = index
                dni = medico['id']['value'] if 'id' in medico and 'value' in medico ['id'] else ''

                try:
                    dni = int(''.join(filter(str.isdigit, dni)))
                except ValueError:
                    dni = None
                
                nombre = medico['name']['first']
                apellido = medico['name']['last']
                matricula = medico['login']['password']
                telefono = medico['phone']
                email = medico['email']
                habilitado = medico['registered']['date']
                
                writer.writerow([medico_id, dni, nombre, apellido, matricula, telefono, email, habilitado])
        print("Archivo CSV creado exitosamente.")
    else:
        print("Error al obtener datos de la API.")

def importar_datos_desde_csv():
    global medicos
    global id_medico
    medicos = []
    with open(ruta_medicos, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['id'] = int(row['id'])
            row['dni'] = int(row['dni'])
            medicos.append(row)
    if len(medicos) > 0:
        id_medico = medicos[-1]['id'] + 1
    else:
        id_medico = 1

def exportar_datos_a_csv():
    with open(ruta_medicos, mode='w', newline='', encoding='utf8') as csvfile:
        campos_nombres = ['id','dni','nombre', 'apellido','matricula','telefono', 'email', 'habilitado']
        writer = csv.DictWriter(csvfile, fieldnames=campos_nombres)
        writer.writeheader()
        for medico in medicos:
            writer.writerow(medico)

def inicializar_medicos():
    global id_medico

    if os.path.exists(ruta_medicos):
       importar_datos_desde_csv()
    else:
      CargarMedicos()

def agregar_medico(dni, nombre, apellido, matricula, telefono, email, habilitado):       
    global id_medico
    medicos.append({
        'id': id_medico,
        'dni': dni,
        'nombre': nombre,
        'apellido': apellido,
        'matricula': matricula,
        'telefono': telefono,
        'email': email,
        'habilitado': habilitado
    })
    id_medico += 1
    exportar_datos_a_csv()
    return medicos[-1]

def obtener_medicos():
    importar_datos_desde_csv()
    return medicos

def obtener_medico_por_id(id):
    for medico in medicos:
        if medico['id'] == id:
            return medico
    return None

def actualizar_medico_por_id(id, dni, nombre, apellido, matricula, telefono, email, habilitado):
    for medico in medicos:
        if medico['id'] == id:
            medico['dni'] = dni
            medico['nombre'] = nombre
            medico['apellido'] = apellido
            medico['matricula'] = matricula
            medico['telefono'] = telefono
            medico['email'] = email
            medico['habilitado'] = habilitado
            exportar_datos_a_csv()
            return medico
    return None

def deshabilirar_medico_por_id(id):#hay que ver que no queden turnos pendientes
    global medicos
    medicos = [medico for medico in medicos if medico['id']!= id]
    if medicos['habilitado'] == True:
        medicos['habilitado'] = False
    exportar_datos_a_csv()
    if len(medicos) > 0:
        return medicos
    else:
        return None

def eliminar_medico_por_id(id):
    global medicos
    medicos = [medico for medico in medicos if medico['id']!= id]
    exportar_datos_a_csv() #incompleto, hay que validar que no tenga turnos pendientes
    if len(medicos) > 0:
        return medicos
    else:
        return None

# def obtener_medico_por_dni(dni):
#     importar_datos_desde_csv()
#     for medico in medicos:
#         if medico['dni'] == dni:
#             return medico
#     return None

# def obtener_medico_por_matricula(matricula):
#     importar_datos_desde_csv()
#     for medico in medicos:
#         if medico['matricula'] == matricula:
#             return medico
#     return None

# def agregar_medico(medico):
#     medicos.append(medico)
#     exportar_datos_a_csv()

# def modificar_medico(id, medico):
#     for medico_en_lista in medicos:
#         if