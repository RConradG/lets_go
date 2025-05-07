from django.contrib import admin
from .models import Vendor, Event, Posts, Follows, TestModel

admin.site.register(Vendor)
admin.site.register(Event)
admin.site.register(Posts)
admin.site.register(Follows)
admin.site.register(TestModel)