from django.contrib import admin
from .models import Collection, Item, Category

admin.site.register(Collection)
admin.site.register(Item)
admin.site.register(Category)