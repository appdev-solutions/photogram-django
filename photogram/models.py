from django.db import models
from accounts.models import User

class Photo(models.Model):
    image = models.CharField(max_length=200)
    caption = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_photos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image
