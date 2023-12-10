import requests
import threading
import json
import data as db
import time

url = f"http://localhost:5000/api/v1/sensors?name="
headers = {
    'Content-Type': 'application/json'
}
results = []
stop_threads = False

def get_or_update_results ():
    """get_or_update_results
    -

    Inicia a atualização em paralelo dos resultados obtidos no banco de dados,
    Esses resultados são os sensores e maquinas cadastradas no banco de dados.
    """
    global results
    global stop_threads

    while True:
        if stop_threads:
            break
        results = db.session.query(db.Sensors, db.Machines).join(db.Machines, db.Sensors.machine_id == db.Machines.id).filter(db.Machines.is_active == True, db.Sensors.is_active == True).all()
        time.sleep(10)

def get_data_sensor(sensor:db.Sensors, machine:db.Machines) -> bool:
    """get_data_sensor
    -

    Args:
        sensor (db.Sensors): sensor para obter e salvar os dados
        machine (db.Machines): machine para salvar os dados

    Returns:
        bool: Retorna True se ocorrer erro
    """
    global url
    global headers
    err = False
    
    try:
        response = requests.request("GET", url + str(sensor.name), headers=headers)
    except Exception as e:
        print("Ocorreu um erro durante a execução do sistema: \n",e)
        err = True
    
    raw_data:dict = response.json()

    timestamp = raw_data.get("timestamp")
    data = raw_data.get("data")

    if timestamp and data:
        raw_data = db.RawDatas(timestamp=timestamp, data=data, machine_id=machine.id, sensor_id=sensor.id)
        db.session.add(raw_data)
        db.session.commit()

    return err
  

def run_app():
    """run_app
    -

    Inicia as requisições para a API a cada 0.3s e salva os dados
    """
    global results
    global stop_threads
    th_results = threading.Thread(target=get_or_update_results)
    th_results.start()
    time.sleep(1)

    try:
        while True:
            time.sleep(0.3) #delay de 0.3s como solicitado

            for sensor, machine in results:
                if get_data_sensor(sensor,machine):
                    break

    except KeyboardInterrupt:
        print("Encerrando...")

    finally:
        stop_threads = True
        th_results.join(10)




if __name__ == "__main__":
    run_app()