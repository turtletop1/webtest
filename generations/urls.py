from django.urls import path
from . import views  

app_name = "generations"

urlpatterns = [                                     
    path('generation/', views.generation , name='generation'),
    path('export_large_csv/', views.export_large_csv , name='export_large_csv'),

    path('poster/<int:post_id>', views.poster , name='poster'),
    path('poster/', views.poster , name='poster'),

    path('some_view/', views.some_view , name='some_view'),
    path('some_view/<int:post_id>', views.some_view , name='some_view_post'),
]