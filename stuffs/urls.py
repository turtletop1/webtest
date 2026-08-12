from django.urls import path
from . import views  

app_name = "stuffs"

urlpatterns = [                                     
    path('create_stuffs/',views.create_stuffs , name='create_stuffs'),        
    path('stuff/', views.stuff , name='stuff'),
    path('create_stuff/', views.create_stuff , name='create_stuff'),
    path('edit_stuff/<int:stuff_id>', views.edit_stuff , name='edit_stuff'),
]