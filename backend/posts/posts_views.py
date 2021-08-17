from django.conf import settings

from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes
from rest_framework.parsers import FormParser, MultiPartParser

from users.models import User
from posts.models import Post, PostComment
from posts.serializers import PostSerializer, ApprovePostSerializer, UpdatePostSerializer, DeletePostSerializer, PostCommentSerializer, DeletePostCommentSerializer
from service_auth.permissions import IsAdminUser, IsUser, IsUserReadOnly


class AllPostViewset(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [IsAdminUser]
  parser_classes = (MultiPartParser, FormParser,)

  def get_queryset(self):
    return Post.objects.order_by('-added')


class UserPostViewset(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [IsUser]
  parser_classes = (MultiPartParser, FormParser,)

  def get_queryset(self):
    return Post.objects.filter(user=self.request.user).order_by('-added')


class PostViewset(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [AllowAny]
  parser_classes = (MultiPartParser, FormParser,)

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = [IsUser]
    elif self.request.method == 'PUT':
      self.permission_classes = [IsUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsUser]
    return super(PostViewset, self).get_permissions()

  def get_queryset(self):
    return Post.objects.filter(post_status=Post.PostStatus.APPROVED).order_by('-added')

  def perform_create(self, serializer):
    serializer.save(user=self.request.user,
                    media_file=self.request.data.get('media_file'), title=self.request.data.get('title'), description=self.request.data.get('description'))


class GetPostsById(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [IsUser | IsAdminUser]
  parser_classes = (MultiPartParser, FormParser,)

  def get_queryset(self):
    return Post.objects.filter(user=self.request.user.id)


class ApprovePostViewset(viewsets.ViewSet):
  queryset = Post.objects.all()
  serializer_class = ApprovePostSerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    post = Post.objects.get(id=self.request.data['post_id'])
    if(self.request.data['post_status'] == Post.PostStatus.APPROVED):
      post.post_status = Post.PostStatus.APPROVED
      post.save()
      return Response("Post approved.", status=status.HTTP_200_OK)
    elif(self.request.data['post_status'] == Post.PostStatus.REJECTED):
      post.post_status = Post.PostStatus.REJECTED
      post.save()
      return Response("Post rejected.", status=status.HTTP_200_OK)


class UpdatePostViewset(viewsets.ViewSet):
  queryset = Post.objects.all()
  serializer_class = UpdatePostSerializer
  permission_classes = [IsUser]
  parser_classes = (MultiPartParser, FormParser,)

  def create(self, request):
    post = Post.objects.get(id=int(self.request.data.get('post_id')))
    if post:
      if(self.request.data.get('media_file')):
        post.title = self.request.data.get('title')
        post.description = self.request.data.get('description')
        post.media_file = self.request.data.get('media_file')
        post.post_status = Post.PostStatus.NEW
        post.save()
        return Response("Post updated.", status=status.HTTP_200_OK)
      else:
        post.title = self.request.data.get('title')
        post.description = self.request.data.get('description')
        post.post_status = Post.PostStatus.NEW
        post.save()
        return Response("Post updated.", status=status.HTTP_200_OK)
    else:
      return Response("Post not found", status=status.HTTP_404_NOT_FOUND)


class DeletePostViewset(viewsets.ViewSet):
  queryset = Post.objects.all()
  serializer_class = DeletePostSerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    post = Post.objects.get(id=int(self.request.data.get('post_id')))
    if post:
      if(post.media_file):
        post.media_file.delete(save=False)
      post.delete()
      return Response("Post deleted.", status=status.HTTP_200_OK)
    else:
      return Response("Post not found", status=status.HTTP_404_NOT_FOUND)


class SaveCommentViewset(viewsets.ViewSet):
  queryset = PostComment.objects.all()
  serializer_class = PostCommentSerializer
  permission_classes = [IsUser]

  def create(self, request):
    if self.request.user:
      if 'post_id' in request.data:
        serializer = self.serializer_class(data=request.data)
        serializer.save(user=self.request.user, post=self.request.data.get('post'), comment=self.request.data.get('comment'))
        return Response({
          'status' : True,
          'detail' : 'Comment created.'
        })
      else:
        return Response({
          'status': False,
          'detail': 'User not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({
        'status': False,
        'detail': 'User not found'
      }, status=status.HTTP_404_NOT_FOUND)


class DeleteCommentViewset(viewsets.ViewSet):
  queryset = PostComment.objects.all()
  serializer_class = DeletePostCommentSerializer
  permission_classes = [IsUser]

  def create(self, request):
    if self.request.user:
      pass
    else:
      return Response({
        'status' : False,
        'detail' : 'User not found'
      }, status=status.HTTP_404_NOT_FOUND)
