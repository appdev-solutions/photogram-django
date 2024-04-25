from django.http import HttpResponseRedirect
from django.contrib import messages
from functools import wraps
from .models import Photo

def user_can_comment(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        photo_id = request.POST.get("photo_id")
        photo = Photo.objects.get(pk=photo_id)
        owner = photo.owner

        # Check if the user is authorized to comment
        if request.user == owner or not owner.private or request.user.leaders().filter(pk=owner.pk).exists():
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, "You are not authorized to comment on this photo.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return wrapper