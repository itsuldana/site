from django.urls import path
from .views import posts

urlpatterns = [
    # News view
    path("", posts.PostListView.as_view(), name="post_list"),
    path("<int:pk>/", posts.PostDetailView.as_view(), name="post_detail"),
]
