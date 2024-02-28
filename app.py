# PROYECTO FINAL DE PROGRAMACION II
# Integrantes:
# D'Onofrio, Daniel
# Ponce, Gabriel
#######

from flask import Flask

from modelos.medicos import inicializar_medicos
from modelos.pacientes import inicializar_pacientes
from modelos.agenda_medicos import inicializar_agenda
from modelos.turnos import inicializar_turnos

from controladores.rutas_medicos import medicos_bp
from controladores.rutas_pacientes import pacientes_bp
from controladores.rutas_agenda_medicos import agenda_bp
from controladores.rutas_turnos import turnos_bp

app = Flask(__name__)

inicializar_medicos()
inicializar_pacientes()
inicializar_agenda()
inicializar_turnos()

app.register_blueprint(medicos_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(agenda_bp)
app.register_blueprint(turnos_bp)

if __name__ == '__main__':
    app.run(debug=True)