from django.urls import path, include
from rest_framework import routers

from posts.posts_views import *

router = routers.DefaultRouter()

router.register('post', PostViewset)
router.register('get-post-by-id', GetPostsById)
router.register('get-all-post', AllPostViewset)
router.register('get-user-post', UserPostViewset)
router.register('approve-post', ApprovePostViewset)
router.register('update-post', UpdatePostViewset)
router.register('delete-post', DeletePostViewset)

urlpatterns = [
    path('', include(router.urls))
]
