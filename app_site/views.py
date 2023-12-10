import pandas as pd
import random

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json

import data as db

colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
    "#aec7e8",
    "#ffbb78",
    "#98df8a",
    "#ff9896",
    "#c5b0d5",
    "#c49c94",
    "#f7b6d2",
    "#c7c7c7",
    "#dbdb8d",
    "#9edae5",
]

# Create your views here.
def home(request):
    results = (db.session.query(db.Sensors, db.Machines)
                .join(db.Machines, db.Sensors.machine_id == db.Machines.id)
                .filter(db.Machines.is_active == True, db.Sensors.is_active == True)
                .all()
                )
    sensors_machines = [ 
        {
            "machine_name" : machine.name,
            "sensor_name": sensor.name,
            "color": random.choice(colors),
        }for sensor,machine in results]
    
    df = pd.DataFrame(sensors_machines)
    df_agrupado = df.groupby('machine_name')
    raw_data = json.loads(df_agrupado.agg(list).to_json(orient="index"))
    
    data = []
    for key in raw_data.keys():
        s = [{
                'name': raw_data[key]['sensor_name'][i],
                'color':raw_data[key]['color'][i]
            }for i in range(len(raw_data[key]['sensor_name']))]
        data.append({
        'name':key,
        'sensores':s})

    #from ipdb import set_trace; set_trace()

    return_data = {
        "machines" : data,
        "labels": range(1,201)
    }

    print(return_data)
    return render(request,"app_site/global/home.html", return_data)



class SensorsMachines(View):    
    def get(self, request, *args, **kwargs):
        data = db.session.query(db.Sensors, db.Machines).join(db.Machines, db.Sensors.machine_id == db.Machines.id).filter(db.Machines.is_active == True, db.Sensors.is_active == True).all()
        
        response_data = [{
            "machine_id" : machine.id,
            "machine": machine.name,
            "sensor_id": sensor.id,
            "sensor": sensor.name
        } for sensor, machine in data] 

        # Retorna uma resposta JSON
        return JsonResponse({"data":response_data})



class DataSensors(View):    
    def get(self, request, *args, **kwargs):
        results = (db.session.query(db.Sensors, db.Machines)
                   .join(db.Machines, db.Sensors.machine_id == db.Machines.id)
                   .filter(db.Machines.is_active == True, db.Sensors.is_active == True)
                   .all()
                   )
        sensors_machines = [ 
            {
                "machine_name" : machine.name,
                "sensor_name": sensor.name,
                "color": random.choice(colors),
            }for sensor,machine in results]
        
        df = pd.DataFrame(sensors_machines)
        df_agrupado = df.groupby('machine_name')
        raw_data = json.loads(df_agrupado.agg(list).to_json(orient="index"))
        
        data = []
        for key in data.keys():
            s = [{
                    'name': data[key]['sensors'][i],
                    'color':data[key]['color'][i]
                }for i in range(len(data[key]['sensors']))]
            data.append({
            'name':key,
            'sensores':s})
       
        return JsonResponse({"data":data})



class ValuesSensor(View):    
    def get(self, request, *args, **kwargs):
        sensor_name = kwargs.get('sensor_name')
        sensor = db.session.query(db.Sensors).filter(db.Sensors.name == sensor_name).first()
        results = db.session.query(db.RawDatas).filter(db.RawDatas.sensor_id == sensor.id).order_by(db.RawDatas.id.desc()).limit(200).all()
        data = [i.data for i in results]
        return JsonResponse({sensor_name:data})