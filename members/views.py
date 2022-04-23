from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegisterView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/register.html'

    def get(self, request):
        form = UserCreationForm()
        return Response({"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        form.is_valid()
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        group = Group.objects.get(name="sub")
        user = authenticate(username=username, password=raw_password)
        user.groups.add(group)
        user.save()
        login(request, user)
        return redirect('home')
