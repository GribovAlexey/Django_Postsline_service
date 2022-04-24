from django.urls import path

from .views import ListPostsView, PostDetailsView

urlpatterns = [
    path("", ListPostsView.as_view(), name="home"),
    path("<int:pk>", PostDetailsView.as_view()),
]
