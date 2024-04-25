from django.views.generic import UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from ..models import Comment
from ..forms import CommentForm

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
