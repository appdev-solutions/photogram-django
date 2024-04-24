from django.urls import path
from .views import PhotoListView, UserDetailView, PhotoCreateView

urlpatterns = [
    path("photos/", PhotoListView.as_view(), name="photos"),
    path("photos/new", PhotoCreateView.as_view(), name="photo_create"),
    path("users/<str:username>/", UserDetailView.as_view(), name="user_detail"),
]