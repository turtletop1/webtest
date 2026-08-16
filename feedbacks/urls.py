from django.urls import path
from . import views  

app_name = "feedbacks"

urlpatterns = [                                     
    path('create_feedback/', views.create_feedback, name='create_feedback'), 
    path('delete_feedback/<int:feedback_id>', views.delete_feedback, name='delete_feedback'), 
    path('feedback/', views.feedback , name='feedback'),
]