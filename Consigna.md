# Trabajo final para promocionar la materia

## Desarrollo de una API REST para la gestión de turnos médicos

### Puntos a desarrollar:

1. Crear una nueva carpeta `turnero` para alojar el proyecto.
2. Crear el entorno virtual `.venv` para el proyecto e instalar `Flask` y `Requests`.
3. Crear el archivo `app.py` y las carpetas `modelos\` (para la gestión de datos) y `controladores\` (para las rutas)
4. En la carpeta `modelos\` crear los archivos que carguen en memoria y gestionen los datos almacenados en los archivos `pacientes.csv`, `medicos.csv`, `agenda_medicos.csv` y `turnos.csv`:
    * médicos: `id, dni, nombre, apellido, matrícula, teléfono, email, habilitado`
    * pacientes: `id, dni, nombre, apellido, teléfono, email, direccion_calle, direccion_numero`
    * agenda_medicos: `id_medico, dia_numero, hora_inicio, hora_fin, fecha_actualizacion` donde "dia_numero" es el numero de día en la semana donde domingo=0 y sábado=6, por lo tanto si un médico atiende lunes y miercoles figurará en dos filas del archivo: en una tendrá dia_numero=1 y la otra tendrá dia_numero=3
    * turnos: `id_medico, id_paciente, hora_turno, fecha_solicitud` . Todos los médicos dan los turnos cada 15 minutos, por lo tanto los posibles turnos son HH:00, HH:15, HH:30 y HH:45

    * Primera carga de datos: en el primer uso los archivos no tendrán datos, los datos del archivo `agenda_medicos.csv` podrán generarlos ustedes con los datos que deseen para el primer uso, pero los archivos `pacientes.csv` y `medicos.csv` deberán ser cargados con los datos que surjan de una consulta a la API pública [https://randomuser.me/](https://randomuser.me/) , pueden encontrar la documentación en: [https://randomuser.me/documentation](https://randomuser.me/documentation) (prestar especial atención a la sección "including/excluding fields" para obtener sólo los datos que requieran) en el código que desarrollen deberán programar el caso en que no existan los archivos de pacientes o médicos para que se realicen estas consultas y los datos se almacenen en los archivos, luego se cargarán siempre los datos de los archivos existentes.
    *Para los DNI deberán adaptar el valor contenido en "id"->"value". Y para la matrícula de los médicos usaremos el valor contenido en "login"->"password" dado que no tenemos un campo relacionado a la matricula, para poder usar este valor de password como matrícula debemos pedirle a la api que lo genere como numero y con una longitud de 6 caracteres (ver documentacion de la api).*

    Observación: Los datos de los médicos, pacientes, agenda y turnos deben cargarse en memoria en listas de diccionarios.
    En el caso de los turnos inicialmente no hay datos cargados en el archivo, deberán cargarse los turnos asignados con el uso de la API.

5. En la carpeta `controladores\` crear los archivos que gestionarán las rutas, definir los blueprints en cada archivo y luego en `app.py` importarlos y registrarlos.
6. Creación de rutas (endpoints), todas las solicitudes recibirán datos en formato JSON (si es que requieren datos):
    * Médicos:
        * Obtener la lista de todos los médicos (`GET`).
        * Obtener detalles de un médico por su ID (`GET`).
        * Agregar un nuevo médico (`POST`).
        * Actualizar la información de un médico por su ID (`PUT`).
        * Deshabilitar un médico (`PUT`). Inhabilitar un médico deberá prohibirle entregar nuevos turnos, pero no influye a los turnos asignados.
    * pacientes:
        * Obtener la lista de todos los pacientes (`GET`).
        * Obtener detalles de un paciente por su ID (`GET`).
        * Agregar un nuevo paciente (`POST`).
        * Actualizar la información de un paciente por su ID (`PUT`).
        * Eliminar un paciente por su ID (`DELETE`). Realizar validaciones antes de eliminar el paciente: no debe tener pendiente una turno.
    * agenda_medicos:
        * Obtener la lista de todos los horarios habilitados para los médicos ordenados por médicos y por numero de día (`GET`). Ejemplo: primero todos los días que atiende el médico con ID=1 y esos dias ordenados del 1 al 5. (Ver ayudita al final de la consigna)
        * Agregar un día y horario de atención de un médico (`POST`).
        * modificar los horarios de atención de un médico (`PUT`).  (Por ejemplo, puede recibir los días que modifica el horario de atención de la forma `[{"dia":1, "hora_inicio" : "10:00", "hora_fin":"17:00"},{"dia":3, "hora_inicio" : "8:00", "hora_fin":"12:00"}]` para indicar que se modifican los horarios de atención de lunes y miercoles - puede haber cualquier combinacion de días de la semana entre el lunes y el viernes, pero se debe verificar que se modifique el horario solamente si el médico trabaja ese día, es decir, no se agregan nuevos dias de atención en esta consulta)
        * eliminar los días de atención de un médico por su ID (`DELETE`). **No importa si hay turnos asignados en el día a eliminar, sino que se elimina de la agenda para que no puedan otorgarse nuevos turnos en ese día.**
    * turnos:
        * Obtener todos los turnos de un médico por su ID (`GET`).
        * Obtener turnos pendientes de un médico por su ID (`GET`).
        * Registrar un nuevo turno (`POST`).  **Los turnos se agendan solamente cuando la fecha del turno está dentro de los próximos 30 días respecto al día actual (Es decir, cada día se pueden otorgar turnos como máximo a 30 días del día actual). Se debe verificar que el médico esté habilitado a dar turnos, que el turno solicitado sea en un día de la semana que el médico trabaja, que el horario del turno solicitado esté dentro del rango horario de atención del médico y que no se haya dado ese turno.** (Ver ayudita al final de la consigna)
        * Registrar la anulación de un turno por su ID (`DELETE`).
7. Persistencia de datos:
    Los datos que irá manejando la API deben actualizarse en los archivos del modelo a medida que se van generando/modificando.

IMPORTANTE: Agrega validaciones para asegurarte de que los datos proporcionados a la API sean correctos y válidos en todo momento, de lo contrario retornar un mensaje de datos incorrectos con un código de respuesta de error.

AYUDITA:

* Ejemplo de datos archivo agenda_medicos:

```text
id_medico, dia_numero, hora_inicio, hora_fin, fecha_actualizacion
1,1,8:00,12:00,2023/11/5
1,3,16:00,21:00,2023/11/5
...
```

* Para saber si el médico trabaja un determinado dia se deberá verificar la información del archivo agenda_medicos, pueden usar el método `strftime` de la clase `datetime` con el parámetro `'%w'` para obtener el número del día de la semana de un objeto datetime. Este método devuelve un **string** donde el domingo es '0' y el sábado es '6'.

* Para comprobar si un horario de turno está en el rango horario de atencion del médico se puede usar la función de la clase `datetime.time` : `datetime.strptime(string_hora, '%H:%M').time()`. donde en `string_hora` tenemos la hora en formato string. Se utiliza `'%H:%M'` en la creación del objeto time para el formato de hora en formato de 24 horas (hora:minuto).

Ejemplos:

```python
import datetime

hoy = datetime.datetime.now() # 9/11/2023
print(hoy.strftime('%w')) # salida: 4

hora_inicio_string = "08:00"
hora_fin_string = "17:00"
hora_a_comparar_string = "12:30"
# Convertir las cadenas de hora a objetos time
hora_a_comparar = datetime.datetime.strptime(hora_a_comparar_string, '%H:%M').time()
hora_inicio = datetime.datetime.strptime(hora_inicio_string, '%H:%M').time()
hora_fin = datetime.datetime.strptime(hora_fin_string, '%H:%M').time()
# Verificar si la hora está dentro del rango
print(hora_a_comparar >= hora_inicio and hora_a_comparar <= hora_fin) # devuelve True
```
