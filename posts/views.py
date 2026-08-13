from django.shortcuts import render ,get_object_or_404 , redirect
from .models import Post , Stuff
from django.core.paginator import Paginator
from .forms import PostForm 
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import F
from django.contrib import messages


from .choices_post import type

def post(request):

    postsss = Post.objects.order_by('-issue_date').filter(status='posting')

    paginator = Paginator(postsss, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)

    context = {"postss": paged_listings}
    return render(request,'posts/post.html',context)


def missing(request):
    postsss = Post.objects.order_by('-issue_date').filter(type='missing',status='posting')

    paginator = Paginator(postsss, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)

    context = {"postss": paged_listings}
    return render(request,'posts/post.html',context)

def discover(request):
    postsss = Post.objects.order_by('-issue_date').filter(type='discover',status='posting')

    paginator = Paginator(postsss, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)

    context = {"postss": paged_listings}
    return render(request,'posts/post.html',context)


def create_post(request):
    
    post_stuffs = Stuff.objects.filter(user=request.user) # Post.objects.filter(stuff__user=request.user)

    if request.method == "POST":
        stuff = request.POST['stuff']
        title = request.POST['title']
        issue_date = request.POST['issue_date']
        due_date = request.POST['due_date']
        status = request.POST['status']
        content = request.POST['content']
        user_id = request.POST['user_id']
        type = request.POST['type']

        post_data = Post(stuff_id=stuff ,title = title ,issue_date = issue_date , due_date=due_date, status=status,content=content,type=type ,user_id=user_id)
    
        post_data.save()
        messages.success(request,'Your request have been submitted')

    context = {
            'post_stuffs': post_stuffs
    }
    
    return render(request,'posts/create_post.html',context)


def user_post(request):
    
    postsss = Post.objects.order_by('-issue_date').filter(user_id = request.user.id) #request = post
                
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


def search(request):
    queryset_list = Post.objects.order_by('-issue_date') 

    if 'keywords' in request.GET:                           
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                Q(content__icontains=keywords) | Q(title__icontains=keywords)
            ) 

    if 'missing_date' in request.GET:                           
        missing_date = request.GET['missing_date']
        if missing_date:
            queryset_list = queryset_list.filter(stuff__missing_date__date=missing_date) # use fk and only __date format

    if 'status' in request.GET:                           
            status = request.GET['status']
            if status:
                queryset_list = queryset_list.filter(status__icontains=status) 

    if 'type' in request.GET:
        type = request.GET['type']
        if type:
            queryset_list = queryset_list.filter(type__iexact=type)

    paginator = Paginator(queryset_list, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)

    context = {"postss": paged_listings, "values": request.GET}
    return render(request, 'posts/post.html', context)
    