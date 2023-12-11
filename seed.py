import data as db
from sqlalchemy.orm import relationship

# Inciando com as tabelas padrão
machine = db.Machines(name="primeira_maquina")
db.session.add(machine)

sensor1 = db.Sensors(name="sensor1", data=40, machine=machine)
sensor2 = db.Sensors(name="sensor2", data=60, machine=machine)
sensor3 = db.Sensors(name="sensor3", data=30, machine=machine)

db.session.add(sensor1)
db.session.add(sensor2)
db.session.add(sensor3)

db.session.commit()

result = db.session.query(db.Sensors, db.Machines).join(db.Machines, db.Sensors.machine_id == db.Machines.id).filter(db.Machines.is_active == True, db.Sensors.is_active == True).all()

print(result)

for sensor, machine in result:
    print(f"Sensor ID: {sensor.id}, Sensor Name: {sensor.name}, Machine ID: {machine.id}, Machine Name: {machine.name}")