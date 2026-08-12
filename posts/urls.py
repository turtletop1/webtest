from django.urls import path
from . import views  

app_name = "posts"

urlpatterns = [                                             
    path('post/', views.post , name='post'),
    path('create_post/', views.create_post , name='create_post'),
]