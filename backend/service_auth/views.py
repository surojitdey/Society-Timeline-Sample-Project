# CAVEAT: we are now using JWT to handle authentication, but in the future we
# may define another way.
# This brings to the views this definition and not to the urls, encapsulating
# this decision.
# from rest_framework_jwt.views import (
#     obtain_jwt_token as get_token,
#     refresh_jwt_token as refresh_token,
# )
from rest_framework_simplejwt import views as jwt_views
from service_auth.serializers import MyTokenObtainPairSerializer
from service_auth.permissions import IsUser, IsAdminUser


class MyTokenObtainPairView(jwt_views.TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer
  permission_classes = []


obtain_jwt_token = MyTokenObtainPairView.as_view()
refresh_jwt_token = jwt_views.TokenRefreshView.as_view()
