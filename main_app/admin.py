from django.contrib import admin
from .models import Vendor, Event, SavedEvents, Address, Posts, Follows

admin.site.register(Vendor)
admin.site.register(Event)
admin.site.register(SavedEvents)
admin.site.register(Address)
admin.site.register(Posts)
admin.site.register(Follows)