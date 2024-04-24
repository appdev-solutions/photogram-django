from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.urls import reverse
from .models import Photo
from accounts.models import User
from .forms import PhotoForm, CommentForm

class PhotoListView(ListView):
    model = Photo
    template_name = "photos/photo_list.html"

class PhotoUpdateView(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photos/photo_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("user_detail", kwargs={"username": self.request.user.username})

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.photo = Photo.objects.get(id=request.POST.get("photo_id"))
            comment.save()
        return super().get(request, *args, **kwargs)