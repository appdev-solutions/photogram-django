from django.views.generic import ListView, DetailView
from .models import Photo
from accounts.models import User

class PhotoListView(ListView):
    model = Photo
    template_name = "photos/photo_list.html"

class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"
