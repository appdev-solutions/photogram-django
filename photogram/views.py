from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .models import Photo
from accounts.models import User
from .forms import PhotoForm

class PhotoListView(ListView):
    model = Photo
    template_name = "photos/photo_list.html"

class PhotoCreateView(CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photos/photo_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("user_detail", kwargs={"username": self.request.user.username})

class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"
