from django.views.generic import DetailView, FormView, ListView
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.contrib import messages
from ..models import Photo
from accounts.models import User
from ..forms import CommentForm

class UserLikesGet(ListView):
    model = Photo
    template_name = "users/user_likes.html"
    context_object_name = "liked_photos"

    def get_queryset(self):
        username = self.kwargs.get("username")
        user = User.objects.get(username=username)
        return user.liked_photos()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class UserLikesPost(SingleObjectMixin, FormView):
    model = User
    form_class = CommentForm
    template_name = "users/user_likes.html"
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

class UserLikesView(View):
    def get(self, request, *args, **kwargs):
        view = UserLikesGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = UserLikesPost.as_view()
        return view(request, *args, **kwargs)

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
