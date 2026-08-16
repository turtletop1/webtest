from django.urls import path
from . import views  

app_name = "comments"

urlpatterns = [                                     
    path('comment/',views.comment , name='comment'),
    path('delete_comment/<int:comment_id>', views.delete_comment , name='delete_comment'),
    path('edit_comment/<int:comment_id>', views.edit_comment , name='edit_comment'),
]