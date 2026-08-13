from django.shortcuts import render
from posts.models import Post

# Create your views here.
def index(request):

    postss = Post.objects.order_by('-issue_date').filter(status='posting')[:3]
    
    context = {"postss": postss}

    return render(request,'pages/index.html', context)
