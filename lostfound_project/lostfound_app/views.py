
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

# lostfound_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import LostItem
from django.db.models import Q
from .forms import LostItemForm, ClaimForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, authenticate

def home(request):
    if request.user.is_authenticated:
        items = LostItem.objects.filter(
            Q(found=False) |
            Q(found=True, posted_by=request.user)
        ).order_by('-date_posted')
    else:
        items = LostItem.objects.filter(found=False).order_by('-date_posted')
    return render(request, 'home.html', {'items': items})

@login_required
def post_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.posted_by = request.user
            lost_item.save()
            return redirect('home')
    else:
        form = LostItemForm()
    return render(request, 'post_item.html', {'form': form})

@login_required
def claim_item(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimed_by = request.user
            claim.save()
            item.found = True
            item.save()
            return redirect('home')
    else:
        form = ClaimForm()
    return render(request, 'claim_item.html', {'form': form, 'item': item})


# Explicit login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    # If ?google=1, redirect to allauth Google login
    if request.GET.get('google') == '1':
        return redirect('/accounts/google/login/')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Explicit signup view
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    # If ?google=1, redirect to allauth Google signup
    if request.GET.get('google') == '1':
        return redirect('/accounts/google/login/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Delete claimed item (only by poster)
from django.contrib.auth.decorators import login_required
@login_required
def delete_claimed_item(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    if item.posted_by != request.user:
        return redirect('home')
    if request.method == 'POST':
        item.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'item': item})
