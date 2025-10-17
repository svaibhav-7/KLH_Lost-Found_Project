from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout

class RestrictEmailToKLHDomain:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # Skip checks for Django admin URLs
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        if request.user.is_authenticated:
            # Allow staff/superusers to pass
            if request.user.is_staff or request.user.is_superuser:
                return self.get_response(request)

            email = (request.user.email or '')
            if not email.endswith('@klh.edu.in'):
                messages.error(request, "Login restricted to @klh.edu.in emails only.")
                logout(request)
                return redirect('/')

        response = self.get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.
        
        return response
