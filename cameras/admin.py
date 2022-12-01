from django.contrib import admin
from .models import Camera
from .models import Upload

admin.site.register(Camera)
admin.site.register(Upload)