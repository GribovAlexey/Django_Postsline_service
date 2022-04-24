from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer


class ListPostsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        form = None
        if request.user.has_perm("blog.add_post"):
            form = PostForm()
        if request.user.has_perm("blog.view_private_posts"):
            displayed_posts = Post.objects.all()
        else:
            displayed_posts = Post.objects.filter(is_public=True).all()
        # serializer = PostSerializer(displayed_posts, many=True)
        return Response({'posts': displayed_posts, "form": form},
                        template_name="home.html")

    def post(self, request):
        if not request.user.has_perm("blog.add_post"):
            return Response("No permission to add a post")
        body = PostForm(request.POST)
        if not body.is_valid():
            return redirect('home')
        body = body.cleaned_data
        new_post = Post(content=body['content'], title=body["title"],
                        author=request.user,
                        is_public=body["is_public"])
        new_post.save()
        return redirect('home')


class PostDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        form = None
        if not request.user.has_perm("blog.view_private_posts"):
            return redirect('home')
        post = Post.objects.get(id=pk)
        if request.user.has_perm(
                "blog.edit_post") and request.user == post.author:
            form = PostForm(PostSerializer(post).data)

        return Response({'post': post, "form": form},
                        template_name="post_detail.html")
        # serializer = PostSerializer(post)
        # return Response(serializer.data)

    def post(self, request, pk):
        if not request.user.has_perm("blog.edit_post"):
            return redirect('home')

        body = PostForm(request.POST)
        if not body.is_valid():
            return redirect('home')
        body = body.cleaned_data

        ed_post = Post.objects.get(id=pk)
        if request.user.id != ed_post.author.id:
            return redirect('home')

        ed_post.content = body["content"]
        ed_post.title = body["title"]
        ed_post.is_public = body["is_public"]
        ed_post.save()
        return redirect('home')

    def delete(self, request, pk):
        if not request.user.has_perm("blog.delete_post"):
            return Response("No permission")
        post = Post.objects.get(id=pk)
        if post is not None and post.author.id != request.user.id:
            return Response("Cant delete. Not an author")
        post.delete()
        return Response("Nice")
