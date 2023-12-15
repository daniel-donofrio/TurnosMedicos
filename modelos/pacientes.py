import requests, csv, os

pacientes = []
id_paciente = 1
ruta_pacientes = 'modelos\\pacientes.csv'

def CargarPacientes():
    url = 'https://randomuser.me/api/?results=25&nat=es'
    ruta_pacientes = 'modelos\\pacientes.csv'
    response = requests.get(url)  # Cambia el número de resultados si quieres más usuarios

    # Verificar si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        data = response.json()  # Obtener los datos en formato JSON
        #print(data)
    # Abrir un archivo CSV en modo escritura
        with open(ruta_pacientes, mode='w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            
            # Escribir encabezados en el archivo CSV
            writer.writerow(['id','dni','nombre', 'apellido', 'telefono', 'email', 'direccion_calle', 'direccion_numero'])
            
            # Iterar a través de los resultados y escribir en el archivo CSV
            for index, paciente in enumerate( data['results'], start=1):
                paciente_id = index
                dni = paciente['id']['value'] if 'id' in paciente and 'value' in paciente ['id'] else ''

            #convertimos el campo dni a digito     
                try:
                    dni = int(''.join(filter(str.isdigit, dni)))
                except ValueError:
                    dni = None
                
                nombre = paciente['name']['first']
                apellido = paciente['name']['last']
                telefono = paciente['phone']
                email = paciente['email']
                direccion_calle = paciente['location']['street']['name']
                direccion_numero = paciente['location']['street']['number']    
                
                # Escribir la información del usuario en una fila del archivo CSV
                writer.writerow([paciente_id, dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero])
        print("Archivo CSV creado exitosamente.")
    else:
        print("Error al obtener datos de la API.")

def importar_datos_desde_csv():
    global pacientes
    global id_paciente
    pacientes = []
    with open(ruta_pacientes, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['id'] = int(row['id'])
            row['dni'] = int(row['dni'])
            row['direccion_numero'] = int(row['direccion_numero'])
            pacientes.append(row)
    if len(pacientes) > 0:
        id_paciente = pacientes[-1]['id'] + 1
    else:
        id_paciente = 1  

def exportar_datos_a_csv():
    with open(ruta_pacientes, mode='w', newline='', encoding='utf8') as csvfile:
        campos_nombres = ['id','dni','nombre', 'apellido', 'telefono', 'email', 'direccion_calle', 'direccion_numero']
        writer = csv.DictWriter(csvfile, fieldnames=campos_nombres)
        writer.writeheader()
        for paciente in pacientes:
            writer.writerow(paciente)

def inicializar_pacientes():
    global id_paciente

    if os.path.exists(ruta_pacientes):
        importar_datos_desde_csv()
    else:
        CargarPacientes()

def agregar_paciente(dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero):
    global id_paciente
    pacientes.append({
        'id': id_paciente,
        'dni': dni,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'email': email,
        'direccion_calle': direccion_calle,
        'direccion_numero': direccion_numero
    })
    id_paciente += 1
    exportar_datos_a_csv()
    return pacientes[-1]

def obtener_pacientes():
    return pacientes

def obtener_paciente_por_id(id):
    for paciente in pacientes:
        if paciente['id'] == id:
            return paciente
    return None

def actualizar_paciente_por_id(id, dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero):
    for paciente in pacientes:
        if paciente['id'] == id:
            paciente['dni'] = dni
            paciente['nombre'] = nombre
            paciente['apellido'] = apellido
            paciente['telefono'] = telefono
            paciente['email'] = email
            paciente['direccion_calle'] = direccion_calle
            paciente['direccion_numero'] = direccion_numero
            exportar_datos_a_csv()
            return paciente
    return None

def eliminar_paciente_por_id(id):
    global pacientes
    pacientes = [paciente for paciente in pacientes if paciente['id']!= id]
    exportar_datos_a_csv() #incompleto, hay que validar que no tenga turnos pendientes
    if len(pacientes) > 0:
        return pacientes
    else:
        return None

def paciente_existe(id):
    for paciente in pacientes:
        if paciente['id'] == id:
            return paciente
    return None 