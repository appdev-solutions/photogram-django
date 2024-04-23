from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "image",
        "owner",
        "created_at",
        "updated_at",
    ]

admin.site.register(Photo, PhotoAdmin)
