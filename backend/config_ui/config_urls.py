from django.urls import path, include
from rest_framework import routers

from config_ui.views import *

router = routers.DefaultRouter()

router.register('contacts', ContactsViewset)
router.register('update-contacts', UpdateContactsViewset)
# router.register('get-user-by-id', GetUserByIdViewset)
# router.register('get-user-by-mobile-number', GetUserByMobileNumberViewset)
# router.register('admin-user', AdminUserViewset)
# router.register('user-family', FamilyViewset)
# router.register('update-user-status', UserStatusUpdateViewset)
# router.register('forgot-password', ForgotPasswordViewset)

urlpatterns = [
    path('', include(router.urls))
]
