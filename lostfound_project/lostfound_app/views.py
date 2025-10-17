from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.contrib import messages

def restrict_klh_email(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            email = request.user.email
            if not email.endswith('@klh.edu.in'):
                messages.error(request, "Login restricted to @klh.edu.in emails only.")
                from django.contrib.auth import logout
                logout(request)
                return redirect('/')
        return get_response(request)
    return middleware
