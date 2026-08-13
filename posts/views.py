from django.shortcuts import render ,get_object_or_404 , redirect
from .models import Post
from django.core.paginator import Paginator
from .forms import PostForm 
from django.contrib.auth.models import User

from .choices_post import type

def post(request):

    postsss = Post.objects.order_by('-issue_date').filter(status='posting')

    paginator = Paginator(postsss, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)

    context = {"postss": paged_listings}
    return render(request,'posts/post.html',context)

def create_post(request):
    return render(request,'posts/create_post.html')


def user_post(request):
    postsss = Post.objects.order_by('-issue_date').filter(user_id = request.user.id)
                
    paginator = Paginator(postsss, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)
                
    context = {"postss": paged_listings}

    return render(request,'posts/user_post.html',context)


def edit_post(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post,user=post.user)

        if form.is_valid():
            form.save()
            return redirect('posts:post')
        
    else:
        form = PostForm(instance=post,user=post.user)

    context = {"form":form , "post":post}
    return render(request, 'posts/edit_post.html',context)



def delete_post(request,post_id):
    contact = get_object_or_404(Post, pk=post_id)
    contact.delete()
    return redirect('posts:post')