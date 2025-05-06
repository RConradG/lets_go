from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

VENDOR_TYPES = (
    ("F", "Food"),
    ("D", "Drink"),
    ("C", "Crafts"),
)

ROLES = (("U", "USER"), ("V", "VENDOR"), ("P", "PROMOTER"))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=1,
        choices=ROLES,
        default=ROLES[0][0],
    )

    created_at = models.DateTimeField(auto_now_add=True)


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendor")
    vendorType = models.CharField(
        max_length=1,
        choices=VENDOR_TYPES,
        default=VENDOR_TYPES[0][0],
    )
    primary_contact_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    business_email = models.EmailField(unique=False)
    # businessAddress = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='business_address')
    # phone_number = PhoneNumberField(region="US")


class Event(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="event")
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
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
    saved_by = models.ManyToManyField(User, related_name="saved_events")
    created_at = models.DateTimeField(auto_now_add=True)


class Follows(models.Model):
    followingUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followedUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"


class TestModel(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image')
