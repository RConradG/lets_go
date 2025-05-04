from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

class Category(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collection-detail', kwargs={'collection_id': self.id})

class Item(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='item')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-estimated_value']

VENDOR_TYPES = (
        ('F', 'Food'),
        ('D', 'Drink'),
        ('C', 'Crafts'),
)

ROLES = (
    ('U', 'USER'),
    ('V', 'VENDOR'),
    ('P', 'PROMOTER')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    email_address = forms.EmailField(required=True)
    role = models.CharField(
        max_length=1,
        choices=ROLES,
        default =ROLES[0][0],
    )
    # foodPreferences
    # following
    # followers
    created_at = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    
class Vendor(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor')
    vendorType = models.CharField(
        max_length=1,
        choices=VENDOR_TYPES,
        default=VENDOR_TYPES[0][0],
    )
    primary_contact_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    business_email = models.EmailField(unique=True)
    businessAddress = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='business_address')
    phone_number = PhoneNumberField(region="US")
    
    
class Event(models.Model):
    # TODO: uncomment vendor_id
    # Don't forget to uncomment vendor_id 
    # vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='event')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location_name = models.CharField(max_length=100)
    location_street_number = models.IntegerField()
    location_street_name = models.CharField(max_length=100)
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=100)
    location_zipcode = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class SavedEvents(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='saved_events')
    saved_at = models.DateTimeField(auto_now_add=True)    

class Follows(models.Model):
    followingUserId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followedUserId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
class Posts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)