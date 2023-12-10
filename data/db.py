from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine

"""Escalabilidade
-

Para que a escabilidade possa ser atendida, será criado as tabelas abaixo.

A relação entre maquinas e sensores é de 1-N, dessa forma, podemos criar duas
tabelas para resolver os problemas de relações.
"""

#Cria a base
class Base(DeclarativeBase):
    pass

#Conexão com banco SQLITE para simplificar a aplicação
conn = "sqlite:///mydatabase.db"
engine = create_engine(conn)

class Sensors(Base):
    """Sensors
    -
    
    Tabela responsável por criar os sensores

    
    >>> id (PK): Id do sensor,
    >>> name: nome do sensor,
    >>> data: Setpoint do sensor,
    >>> machine (FK): Id da maquina, 
    >>> is_active: Verifica se o sensor está ativo. 
    """
    __tablename__ = "sensor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(Integer)
    # timestamp = Column(Integer) #FIXME 
    is_active = Column(Boolean, default=True)

    # relação estrangeira com a tabela machine
    machine_id = Column(Integer, ForeignKey('machine.id'))
    machine = relationship("Machines", back_populates="sensors")

    #Cria relaçao com a tabela raw_data 
    raw_data = relationship("RawDatas", back_populates="sensors")


class Machines(Base):
    """Machines
    -
    
    Tabela responsável por criar os as maquinas\n

    
    >>> id (PK): Id da maquina,
    >>> name: nome da maquina,
    >>> is_active: Verifica se a maquina está ativo. 
    """
    __tablename__ = "machine"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)

    #Cria relação com a tabela sensor
    sensors = relationship("Sensors", back_populates="machine")

    #Cria relaçao com a tabela raw_data
    raw_data = relationship("RawDatas", back_populates="machines")


class RawDatas(Base):
    """RawDatas
    -
    
    Tabela responsável por guardar os dados dos sensores

    
    >>> id (PK): Id da raw_data,
    >>> timestamp: timestamp da consulta,
    >>> data: Dado obtido do sensor.
    >>> machine_id (FK): Id da maquina.
    >>> sensor_id (FK): Id do sensor.
    """
    __tablename__ = "raw_data"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer) #FIXME 
    data = Column(Integer)

    # Relação estrangeira com a tabela machine
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensors = relationship("Sensors", back_populates="raw_data")

    # Relação estrangeira com a tabela machine
    machine_id = Column(Integer, ForeignKey('machine.id'))
    machines = relationship("Machines", back_populates="raw_data")


# Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()