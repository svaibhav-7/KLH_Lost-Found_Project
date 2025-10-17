from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class LostItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lost_items/')
    date_posted = models.DateTimeField(auto_now_add=True)
    found = models.BooleanField(default=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Claim(models.Model):
    item = models.ForeignKey(LostItem, on_delete=models.CASCADE)
    claimed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    claim_message = models.TextField()
    claimed_on = models.DateTimeField(auto_now_add=True)
