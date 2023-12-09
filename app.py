import random

from flask import Flask, request, jsonify
from time import time

import data as db

app = Flask(__name__)


#Obtem informações de todos os sensores
sensors = {}
for row in db.session.query(db.Sensors).all():
    field = {
        'name': row.name,
        'data': row.data,
        'timestamp': int(time() * 1000)
    }
    sensors[row.name] = field

    
# sensors = {
#     'sensor1': {
#         'name': 'sensor1',
#         'data': 40,
#         'timestamp': int(time() * 1000)
#     },
#     'sensor2': {
#         'name': 'sensor2',
#         'data': 60,
#         'timestamp': int(time() * 1000)
#     },
#     'sensor3': {
#         'name': 'sensor3',
#         'data': 30,
#         'timestamp': int(time() * 1000)
#     },
# }


@app.route('/api/v1/sensors', methods=['GET'])
def get_sensor_data():
    name = request.args.get('name')
    r = random.randint(-2, 2)

    sensor = db.session.query(db.Sensors).filter(db.Sensors.name == name).first()
    
    #Verifica se contém o sensor salvo
    if not sensor:
        return {
            "message": f"Não foi encontrado o sensor com esse nome: {sensor}"
        },404

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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
