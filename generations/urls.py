from django.urls import path
from . import views  

app_name = "generations"

urlpatterns = [                                     
    path('generation/', views.generation , name='generation'),
    path('export_large_csv/', views.export_large_csv , name='export_large_csv'),
]