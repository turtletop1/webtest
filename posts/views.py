from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator

def post(request):

    postsss = Post.objects.order_by('-issue_date').filter(status='posting')

    paginator = Paginator(postsss, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)

    context = {"postss": paged_listings}
    return render(request,'posts/post.html',context)

def create_post(request):
    return render(request,'posts/create_post.html')
