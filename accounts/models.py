from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=150)
    private = models.BooleanField(default=True)
    avatar_image = models.CharField(max_length=200, blank=True, null=True)

    def liked_photos(self):
        # to prevent circular imports (User is imported in our other models file)
        # we only import the Photo model inside the method
        from photogram.models import Photo
        return Photo.objects.filter(likes__fan=self)
    
    def leaders(self):
        return User.objects.filter(sent_follow_requests__recipient=self, sent_follow_requests__status="accepted")

    def followers(self):
        return User.objects.filter(received_follow_requests__sender=self, received_follow_requests__status="accepted")

    def feed(self):
        from photogram.models import Photo
        leaders = self.leaders()
        return Photo.objects.filter(owner__in=leaders)

    def discover(self):
        from photogram.models import Photo
        leaders = self.leaders()
        photos = Photo.objects.filter(likes__fan__in=leaders).distinct()
        return photos
