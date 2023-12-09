import requests
import json
import data as db
import time

url = f"http://localhost:5000/api/v1/sensors?name="
headers = {
    'Content-Type': 'application/json'
}

def get_data_sensor(sensor:db.Sensors, machine:db.Machines):
    global url
    global headers

    response = requests.request("GET", url + str(sensor.name), headers=headers)

    data:dict = response.json()

    raw_data = db.RawDatas(timestamp=data.get("timestamp"), data=data.get("data"), machine_id=machine.id, sensor_id=sensor.id)
    db.session.add(raw_data)
    db.session.commit()
  


def run_app():
    results = db.session.query(db.Sensors, db.Machines).join(db.Machines, db.Sensors.machine_id == db.Machines.id).filter(db.Machines.is_actve == True, db.Sensors.is_actve == True).all()
        
    while True:
        time.sleep(0.3)

        ### Implementar paralelismo #FIXME
        for sensor, machine in results:
            get_data_sensor(sensor,machine)



if __name__ == "__main__":
    run_app()