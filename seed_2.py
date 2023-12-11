import data as db
from sqlalchemy.orm import relationship



# Inciando com as tabelas padrão

machine = db.Machines(name="primeira_maquina")
machine_2 = db.Machines(name="Esteira")
machine_3 = db.Machines(name="Exaustor")
machine_4 = db.Machines(name="Ventilador")
db.session.add(machine)
db.session.add(machine_2)
db.session.add(machine_3)
db.session.add(machine_4)


sensor1 = db.Sensors(name="sensor1", data=40, machine=machine)
sensor2 = db.Sensors(name="sensor2", data=60, machine=machine)
sensor3 = db.Sensors(name="sensor3", data=30, machine=machine)
db.session.add(sensor1)
db.session.add(sensor2)
db.session.add(sensor3)


sensor21 = db.Sensors(name="velocidade", data=100, machine=machine_2)
sensor22 = db.Sensors(name="temperatura", data=30, machine=machine_2)
db.session.add(sensor21)
db.session.add(sensor22)


sensor31 = db.Sensors(name="rotação", data=60, machine=machine_3)
sensor32 = db.Sensors(name="temperatura", data=95, machine=machine_3)
db.session.add(sensor31)
db.session.add(sensor32)



sensor41 = db.Sensors(name="temperatura", data=25, machine=machine_4)
db.session.add(sensor41)


db.session.commit()

# result = db.session.query(db.Sensors, db.Machines).join(db.Machines, db.Sensors.machine_id == db.Machines.id).filter(db.Machines.is_active == True, db.Sensors.is_active == True).all()

# print(result)

# for sensor, machine in result:
#     print(f"Sensor ID: {sensor.id}, Sensor Name: {sensor.name}, Machine ID: {machine.id}, Machine Name: {machine.name}")