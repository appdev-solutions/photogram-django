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
    
    def fans(self):
        return User.objects.filter(likes__photo=self)

class Like(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FollowRequest(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_follow_requests")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_follow_requests")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
