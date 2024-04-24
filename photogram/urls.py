from django.urls import path
from .views import PhotoListView, UserDetailView

urlpatterns = [
    path("photos/", PhotoListView.as_view(), name="photos"),
    path("users/<str:username>/", UserDetailView.as_view(), name="user_detail"),
]