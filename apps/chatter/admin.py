from django.contrib import admin
from apps.chatter import models

# Register your models here.
admin.site.register(models.Room)
admin.site.register(models.Message)