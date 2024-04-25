from django.views.generic import (
    ListView, DeleteView, CreateView, UpdateView
)
from django.urls import reverse
from django.contrib import messages
from ..models import Photo
from ..forms import PhotoForm

class PhotoListView(ListView):
    model = Photo
    template_name = "photos/photo_list.html"

class PhotoUpdateView(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photos/photo_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Photo was successfully updated.")
        return response
    
    def get_success_url(self):
        return reverse("user_detail", kwargs={"username": self.request.user.username})
    
    def get_queryset(self):
        # Ensure that a user can only delete their own photos
        query_set = super().get_queryset()
        return query_set.filter(owner=self.request.user)

class PhotoCreateView(CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photos/photo_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Photo was successfully created.")
        return response
    
    def get_success_url(self):
        return reverse("user_detail", kwargs={"username": self.request.user.username})

class PhotoDeleteView(DeleteView):
    model = Photo

    def get_success_url(self):
        return reverse("user_detail", kwargs={"username": self.request.user.username})
    
    def get_queryset(self):
        # Ensure that a user can only delete their own photos
        query_set = super().get_queryset()
        return query_set.filter(owner=self.request.user)
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Photo was successfully deleted.")
        return response