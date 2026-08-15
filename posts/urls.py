from django.urls import path
from . import views  

app_name = "posts"

urlpatterns = [                                     
    path('post_detail/<int:post_id>', views.post_detail, name='post_detail'), 
    path('post_comment_create/', views.post_comment_create, name='post_comment_create'), 

    path('post/', views.post , name='post'),
    path('create_post/', views.create_post , name='create_post'),
    path('user_post/', views.user_post , name='user_post'),
    path('edit_post/<int:post_id>', views.edit_post , name='edit_post'),
    path('delete_post/<int:post_id>', views.delete_post , name='delete_post'),
    path('search/', views.search , name='search'),
    path('missing/', views.missing , name='missing'),
    path('discover/', views.discover , name='discover'),
]