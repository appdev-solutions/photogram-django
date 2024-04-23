from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    # the Meta class is used to add to the default UserCreationForm fields
    class Meta:
        model = User
        fields = ("username", "email", "name", "private",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "name", "private",)
