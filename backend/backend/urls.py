from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from service_auth.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user-api/v-1/', include('users.user_urls'), name='user-api'),
    path('post-api/v-1/', include('posts.posts_urls'), name='posts-api'),
    path('config-api/v-1/', include('config_ui.config_urls'), name='config-api'),
    path('events-api/v-1/', include('events.events_urls'), name='events-api'),
    path('complaints-and-grievances-api/v-1/',
         include('posts.complaints_urls'), name='complaints-and-grievances-api'),
    path('api/token/', obtain_jwt_token, name='token_obtain_pair'),
    path('api/token/refresh/', refresh_jwt_token, name='token_refresh')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
