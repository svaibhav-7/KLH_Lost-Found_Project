from django.contrib import admin

# Register your models here.
# lostfound_app/admin.py
from django.contrib import admin
from .models import LostItem, Claim

admin.site.register(LostItem)
admin.site.register(Claim)
