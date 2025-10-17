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
from .forms import LostItemForm, ClaimForm
from django.contrib.auth.decorators import login_required

def home(request):
    items = LostItem.objects.all().order_by('-date_posted')
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
