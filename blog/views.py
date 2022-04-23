import json

from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


class ListPostsView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        if request.user.has_perm("blog.view_private_posts"):
            displayed_posts = Post.objects.all()
        else:
            displayed_posts = Post.objects.filter(is_public=True).all()
        serializer = PostSerializer(displayed_posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.has_perm("blog.add_post"):
            return Response("No permission to add a post")
        body = json.loads(request.body)
        new_post = Post(content=body['content'], title=body["title"],
                        author=User.objects.get(id=1),
                        is_public=body["is_public"])
        new_post.save()
        return Response("Ok")


class PostDetailsView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, pk):
        if not request.user.has_perm("blog.view_private_posts"):
            return Response("No permission to view this post")
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.has_perm("blog.edit_post"):
            return Response("No permission")

        body = json.loads(request.body)
        ed_post = Post.objects.get(id=pk)
        if request.user.id != ed_post.author.id:
            return Response("Can't edit. Not an author")

        ed_post.content = body["content"]
        ed_post.title = body["title"]
        ed_post.is_public = body["is_public"]
        ed_post.save()
        return Response("Saved")

    def delete(self, request, pk):
        if not request.user.has_perm("blog.delete_post"):
            return Response("No permission")
        post = Post.objects.get(id=pk)
        if post is not None and post.author.id != request.user.id:
            return Response("Cant delete. Not an author")
        post.delete()
        return Response("Nice")
