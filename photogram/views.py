from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Photo

class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = "photos/photo_list.html"
