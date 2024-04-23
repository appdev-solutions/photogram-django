from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class UserEditView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy("edit_profile")

    def get_object(self, queryset=None):
        return self.request.user
