import random

from flask import Flask, request, jsonify
from time import time

import data as db

app = Flask(__name__)

def check_sensor(sensor:db.Sensors):
    machine = db.session.query(db.Machines).filter(db.Machines.id == sensor.machine_id).first()
    return sensor.is_active and machine.is_active

@app.route('/api/v1/sensors', methods=['GET'])
def get_sensor_data():
    name = request.args.get('name')
    r = random.randint(-2, 2)
   
    sensor = db.session.query(db.Sensors).filter(db.Sensors.name == name).first()
    
    #Verifica se contém o sensor salvo
    if not sensor:
        return {
            "menssagem": f"Não foi encontrado o sensor com esse nome: {sensor}"
        },404
 
    if not check_sensor(sensor):
        return {
            "menssagem": f"Sensor desativado"
        }

    return {
        'name': sensor.name,
        'data': sensor.data + r,
        'timestamp': int(time() * 1000)
    }


@app.route('/api/v1/sensors', methods=['POST'])
def set_points_sensor():
    data = request.json
    sensor = data.get('sensor')
    setpoint = data.get('setpoint')

    # Obtem o sensor, se não contem o sensor salvo retorna mensagem de erro
    sensor_db = db.session.query(db.Sensors).filter(db.Sensors.name == sensor).first()
    if not sensor_db:
        return {
            "menssagem" : f"Não foi encontrado o sensor com esse nome: {sensor}"
        },404

    #Atualiza o sensor
    sensor_db.data = setpoint
    db.session.commit()
    return jsonify(success=True)

@app.post('/api/v1/machine')
def creat_machine():
    data:dict = request.json

    machine_name = data.get("name")
    machine_active = data.get("is_active")

    if machine_name and machine_active:
        import pdb;pdb.set_trace()
        machine = db.Machines(name=machine_name,is_active=machine_active)
        db.session.add(machine)
        db.session.commit()

        return {
            "menssagem" : f"{machine_name} criado"
        },201

    return {
        "menssagem": "Necessário enviar os campos 'name' e 'is_active'"
    },400


@app.post('/api/v1/machine/<name>')
def creat_sensor(name):
    machine = db.session.query(db.Machines).filter(db.Machines.name == name).first()
    if not machine:
        return {
            "message": f"Não foi encontrado maquina com esse nome: {name}"
        },404

    data:dict = request.json

    sensor_name = data.get("name")
    sensor_data = data.get("data")
    sensor_active = data.get("is_active",True)

    if sensor_name and sensor_data:
        sensor = db.Sensors(name=sensor_name, data=sensor_data, is_active=sensor_active, machine=machine)
        db.session.add(sensor)
        db.session.commit()

        return {
            "menssagem" : f"{sensor_name} criado"
        },201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
