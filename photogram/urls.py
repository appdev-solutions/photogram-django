from django.urls import path
from .views import (
    PhotoListView, UserDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView,
    CommentUpdateView, CommentDeleteView, UserLikesView
)

urlpatterns = [
    path("photos/", PhotoListView.as_view(), name="photos"),
    path("photos/new", PhotoCreateView.as_view(), name="photo_create"),
    path("photos/<int:pk>/edit", PhotoUpdateView.as_view(), name="photo_edit"),
    path("photos/<int:pk>/delete/", PhotoDeleteView.as_view(), name="photo_delete"),
    path("users/<str:username>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<str:username>/likes/", UserLikesView.as_view(), name="user_likes"),
    path("comments/<int:pk>/edit", CommentUpdateView.as_view(), name="comment_edit"),
    path("comments/<int:pk>/delete", CommentDeleteView.as_view(), name="comment_delete"),
]
