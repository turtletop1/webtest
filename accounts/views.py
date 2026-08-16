from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages ,auth

# https://docs.djangoproject.com/en/6.0/ref/contrib/auth/

def login(request):                           
    if request.method == "POST":
        username = request.POST["username"]  
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)    

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'You are now logged in')
            return redirect('pages:index')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('accounts:login')
        
    return render(request, 'accounts/login.html')       



def register(request):                                  
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'That username is taken')
                return render(request, 'accounts/register.html')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'That email is being used')
                    return render(request, 'accounts/register.html')
                else:
                    user = User.objects.create_user(username=username,email=email.lower(),password=password,first_name=first_name,last_name=last_name)
                    user.save()
                    messages.success(request,'you are now registered and can log in')
                    return redirect('accounts:login')
        else:   
            messages.error(request,'Passwords do not match')
            return redirect('accounts:register')  
    else:
        return render(request,'accounts/register.html')  



def logout(request):
    if request.method == "POST":                # 出於安全考量，通常建議登出操作使用 POST 方法
        auth.logout(request)                    # 清除 Session，完成登出操作
        return redirect('pages:index')



def dashboard(request):
    
    user_contacts = User.objects.filter(id = request.user.id)    

    context={"contacts":user_contacts}      

    return render(request, 'accounts/dashboard.html',context)



def change_user_info(request):
    
    user = request.user    
    context = {'user': user}

    if request.method == 'POST':
        user_id = request.POST['user_id']
        email = request.POST['email']
            
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
    
        password = request.POST['password']
        old_password = request.POST['password2']

        if user.check_password(old_password):

            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            password_changed = False
            if password:
                user.set_password(password) 
                password_changed = True

            user.save()

            if password_changed:
                auth.update_session_auth_hash(request, user)

            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('accounts:change_user_info')
        else:   
            messages.error(request,'Passwords do not match')
            return redirect('accounts:change_user_info')

    return render(request, 'accounts/change_user_info.html', context)