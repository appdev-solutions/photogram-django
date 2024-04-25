from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, DeleteView
from django.views import View
from django.contrib import messages
from .models import Photo, Comment
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
        response = super().form_valid(form)
        messages.success(self.request, "Comment was successfully created.")
        return response
    
    def get_success_url(self):
        return reverse("user_detail", kwargs={"username": self.object.username})

class UserDetailView(View):
    def get(self, request, *args, **kwargs):
        view = UserDetailGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = UserDetailPost.as_view()
        return view(request, *args, **kwargs)

class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_update.html"
    # Add an attribute to store the photo object
    photo = None

    def get_queryset(self):
        # Ensure that a user can only update their own comments
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        # Store the photo object when the comment form is fetched (GET)
        self.object = self.get_object()
        self.photo = self.object.photo
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Store the photo object when the comment is submitted (POST)
        self.object = self.get_object()
        self.photo = self.object.photo
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self):
        # Redirect to the photo owner's user detail page
        return reverse("user_detail", kwargs={"username": self.photo.owner.username})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_button_text"] = "Update Comment"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Comment was successfully updated.")
        return response

class CommentDeleteView(DeleteView):
    model = Comment

    def get_queryset(self):
        # Ensure that a user can only delete their own comments
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
    
    def get_success_url(self):
        # Redirect to the user's page where the comment was deleted.
        photo = self.get_object().photo
        return reverse("user_detail", kwargs={"username": photo.owner.username})
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Comment was successfully deleted.")
        return response
