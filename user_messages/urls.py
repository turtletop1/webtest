from django.urls import path
from . import views

app_name = 'user_messages'

urlpatterns = [
    path('user_message/<str:user_type>', views.user_message , name='user_message'),
    path('user_message/', views.user_message , name='user_message'),
    path('message_user_delete/<int:user_message_id>', views.message_user_delete , name='message_user_delete'),
    path('create_message/<int:receiver_id>', views.create_message , name='create_message'),
]