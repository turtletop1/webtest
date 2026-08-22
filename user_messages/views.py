from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from .models import User_message


@login_required
def user_message(request,user_type='receiver'):

    if user_type == 'sender':
        msg_user = User_message.objects.filter(sender=request.user).order_by('-date')
    else:
        msg_user = User_message.objects.filter(receiver=request.user).order_by('-date')

    paginator = Paginator(msg_user, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)

    context = {"msg_users": paged_listings ,"user_type":user_type}

    return render(request, 'user_messages/user_message.html', context)


@login_required
def message_user_delete(request, user_message_id):

    contact = get_object_or_404(User_message, pk=user_message_id)
    
    if contact.receiver == request.user or contact.sender == request.user:
        contact.delete()
        messages.success(request, "success。")

        
    return redirect('user_messages:user_message' ,user_type='receiver')


@login_required
def create_message(request, receiver_id):

    receiver = get_object_or_404(User, id=receiver_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content:
            User_message.objects.create(
                sender=request.user,   
                receiver=receiver,      
                content=content
            )
            messages.success(request, f"success send to {receiver.username}")
            return redirect('user_messages:user_message',user_type='sender')
        else:
            messages.error(request, "Please input data")

    context = {"receiver": receiver}

    return render(request, 'user_messages/create_message.html', context)