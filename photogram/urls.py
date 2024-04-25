from django.urls import path
from .views import (
    PhotoListView, UserDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView
)

urlpatterns = [
    path("photos/", PhotoListView.as_view(), name="photos"),
    path("photos/new", PhotoCreateView.as_view(), name="photo_create"),
    path("photos/<int:pk>/edit", PhotoUpdateView.as_view(), name="photo_edit"),
    path("photos/<int:pk>/delete/", PhotoDeleteView.as_view(), name="photo_delete"),
    path("users/<str:username>/", UserDetailView.as_view(), name="user_detail"),
]