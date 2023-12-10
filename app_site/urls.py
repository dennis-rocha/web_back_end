from django.urls import path
from app_site.views import home,SensorsMachines, DataSensors,ValuesSensor

urlpatterns = [
    path('', home),
    path('data/', SensorsMachines.as_view(), name='data'),
    path('sensors/', DataSensors.as_view(), name='sensors'),
    path('sensors/<str:sensor_name>/', ValuesSensor.as_view(), name='values'),
]