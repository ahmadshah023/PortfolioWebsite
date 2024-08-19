from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import qrcode
from io import BytesIO
from django.http import HttpResponse
import barcode
from barcode.writer import ImageWriter
import pyshorteners


# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken already!')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken already!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords did not match!')
            return redirect('signup')
        return redirect('index')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, '   error !  Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def about(request):
    return render(request, 'about.html')

def code(request):
    return render(request, 'code.html')
def qrcode_view(request):
    if request.method == 'POST':
        data = request.POST.get('data')  # Correct way to get POST data in Django
        if data:
            img = qrcode.make(data)
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            return HttpResponse(buffer.getvalue(), content_type="image/png")

    return render(request, 'qrcode_view.html')

# Barcode Generation

def barcode_view(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        CODE128 = barcode.get_barcode_class('code128')
        code = CODE128(data, writer=ImageWriter())
        buffer = BytesIO()
        code.write(buffer)

        return HttpResponse(buffer.getvalue(), content_type='image/png')

    return render(request, 'barcode.html')


# URL Shortening

def URLshorten(request):
    shortened_url = None
    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        s = pyshorteners.Shortener()
        shortened_url = s.tinyurl.short(long_url)

    return render(request, 'urlshorten.html', {'shortened_url': shortened_url})
