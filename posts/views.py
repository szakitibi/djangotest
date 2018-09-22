from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Post
from .permissions import CustomPostPermission
from .serializers import UserSerializer, PostSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows users to be viewed or edited. """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (CustomPostPermission, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, likes=0, dislikes=0)

    @detail_route(methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes += 1
        post.save()
        return Response({'detail': 'Like saved!'}, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def dislike(self, request, pk=None):
        post = self.get_object()
        post.dislikes += 1
        post.save()
        return Response({'detail': 'Dislike saved!'}, status=status.HTTP_200_OK)
