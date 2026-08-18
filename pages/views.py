from django.shortcuts import render
from posts.models import Post
from stuffs.choices_stuff import district_choices

# Create your views here.
def index(request):

    postss = Post.objects.order_by('-issue_date').filter(status='posting')[:6]
    
    context = {"postss": postss,"district_choices":district_choices}

    return render(request,'pages/index.html', context)
