from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import redirect

class KLHSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = (
            sociallogin.account.extra_data.get('email')
            or (sociallogin.user and sociallogin.user.email)
            or ''
        )
        if not email.endswith('@klh.edu.in'):
            messages.error(request, 'Login restricted to @klh.edu.in emails only.')
            raise ImmediateHttpResponse(redirect('/'))
