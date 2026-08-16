from django.shortcuts import render,redirect ,get_object_or_404
from .models import Feedback
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
#from .forms import StuffForm 

def feedback(request):

    if request.user.is_staff == True:
        feedbacks = Feedback.objects.order_by('-date')
    else:
        feedbacks = Feedback.objects.order_by('-date').filter(user_id = request.user.id)
        
    paginator = Paginator(feedbacks, 6)            
    page_number = request.GET.get('page')              
    paged_listings = paginator.get_page(page_number)
            
    context = {"feedbacks": paged_listings}
    return render(request,'feedbacks/feedback.html',context)


def delete_feedback(request,feedback_id):
    contact = get_object_or_404(Feedback, pk=feedback_id)
    contact.delete()
    return redirect('feedbacks:feedback')


def create_feedback(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        content = request.POST['content']
        title = request.POST['title']
    
        fb_data = Feedback(title=title ,user_id = user_id ,content = content )
    
        fb_data.save()
        messages.success(request,'Your request have been submitted')
    
        return render(request,'feedbacks/create_feedback.html')
    return render(request,'feedbacks/create_feedback.html')
    
