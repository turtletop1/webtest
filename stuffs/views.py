from django.shortcuts import render,redirect ,get_object_or_404
from .models import Stuff
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from .choices_stuff import district_choices,type
from .forms import StuffForm 

def stuff(request):
    stuffs = Stuff.objects.order_by('-missing_date').filter(user_id = request.user.id)
            
    paginator = Paginator(stuffs, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)
            
    context = {"stuffs": paged_listings}
    return render(request,'stuffs/stuff.html',context)


def create_stuff(request):
        context = {"type":type , "district_choices":district_choices}

        return render(request,'stuffs/create_stuff.html',context)


def create_stuffs(request):
    if request.method == "POST":
        name = request.POST['name']
        type = request.POST['type']
        district = request.POST['district']
        location = request.POST['location']
        missing_date = request.POST['missing_date']
        description = request.POST['description']
        user_id = request.POST['user_id']

        photo = request.FILES.get('photo')

        stuff_data = Stuff(name=name ,type = type ,district = district , location=location, missing_date=missing_date,description=description,photo_main=photo ,user_id=user_id )

        stuff_data.save()
        messages.success(request,'Your request have been submitted')

        return render(request,'stuffs/create_stuff.html')


def edit_stuff(request,stuff_id):
    stuff = get_object_or_404(Stuff, pk=stuff_id)

    if request.method == "POST":
        form = StuffForm(request.POST, request.FILES, instance=stuff)

        if form.is_valid():
            form.save()
            return redirect('stuffs:stuff')
        
    else:
        form = StuffForm(instance=stuff)

    context = {"form":form , "stuff":stuff}
    return render(request, 'stuffs/edit_stuff.html',context)


def delete_stuff(request,stuff_id):
    contact = get_object_or_404(Stuff, pk=stuff_id)
    contact.delete()
    return redirect('stuffs:stuff')