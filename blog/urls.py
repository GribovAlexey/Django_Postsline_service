from django.urls import path

from .views import ListPostsView, PostDetailsView

urlpatterns = [
    path("post/", ListPostsView.as_view(), name="home"),
    path("post/<int:pk>", PostDetailsView.as_view()),
]
