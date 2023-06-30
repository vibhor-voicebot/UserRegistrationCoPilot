from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from validate_email import validate_email
from .models import Profile
from .forms import LoginForm, SignUpForm
from django.core.mail import EmailMessage
from django.conf import settings
from .decorators import auth_user_should_not_access
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
import threading
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

@auth_user_should_not_access
def Login(request):
    form = SignUpForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'Login.html')

        login(request, user)

        return redirect(reverse('Dashboard'))

    return render(request, 'Login.html', {'form':form})

@auth_user_should_not_access
def Register(request):
    form = SignUpForm()

    if request.method == "POST":
        context = {'has_error': False}
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 6:
            messages.error(request, 'Password should be at least 6 characters for greater security')
            return redirect('Register')

        if password1 != password2:
            messages.error(request, 'Password Mismatch! Your Passwords Do Not Match')
            return redirect('Register')

        if not username:
            messages.error(request, 'Username is required!')
            return redirect('Register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is taken! Choose another one')

            return render(request, 'Register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is taken! Choose another one')

            return render(request, 'Register.html')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.save()
        messages.success(request, 'Sign Up Successful!')
        return redirect('Register')

    return render(request, 'Register.html', {'form':form})

def Logout(request):
    
    logout(request)
    messages.success(request, 'Successfully Logged Out!')

    return redirect(reverse('Login'))

def Dashboard(request):
    return render(request, 'Dashboard.html')