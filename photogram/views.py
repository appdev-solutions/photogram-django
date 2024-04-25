from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, DeleteView
from django.views import View
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
        return super().form_valid(form)
    
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

class UserDetailGet(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class UserDetailPost(SingleObjectMixin, FormView):
    model = User
    form_class = CommentForm
    template_name = "users/user_detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.photo = Photo.objects.get(id=self.request.POST.get("photo_id"))
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("user_detail", kwargs={"username": self.object.username})

class UserDetailView(View):
    def get(self, request, *args, **kwargs):
        view = UserDetailGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = UserDetailPost.as_view()
        return view(request, *args, **kwargs)