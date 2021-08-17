from django.urls import path, include
from rest_framework import routers

from users.views import *

router = routers.DefaultRouter()

router.register('user', UserViewset)
router.register('update-user', UpdateUserViewset)
router.register('get-all-users', GetAllUserViewset)
router.register('get-user', GetUserViewset)
router.register('get-user-by-id', GetUserByIdViewset)
router.register('get-user-by-mobile-number', GetUserByMobileNumberViewset)
router.register('admin-user', AdminUserViewset)
router.register('user-family', FamilyViewset)
router.register('update-user-status', UserStatusUpdateViewset)
router.register('forgot-password', ForgotPasswordViewset)
router.register('update-password', UpdatePasswordViewset)
router.register('get-approved-user', GetApprovedUserViewset)
# router.register('sent-otp', SendOTPViewset, basename='OTP')

urlpatterns = [
    path('', include(router.urls)),
    path('sent-otp/', SendOTPViewset.as_view(), name='sent-otp'),
    path('verify-otp/', VerifyOTPViewset.as_view(), name='verify-otp'),
]
