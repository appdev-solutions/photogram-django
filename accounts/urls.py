from django.urls import path
from .views import SignUpView, UserEditView

urlpatterns = [
    path("edit_profile/", UserEditView.as_view(), name="edit_profile"),
    path("signup/", SignUpView.as_view(), name="signup"),
]