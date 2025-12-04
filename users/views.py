from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, f'Account created for {username}!')
        return redirect('loops_list')
    
    return render(request, 'users/register.html')