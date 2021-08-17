from django.urls import path, include
from rest_framework import routers

from posts.complaints_views import *

router = routers.DefaultRouter()

router.register('complaints-and-grievances', ComplaintsAndGrievancesViewset)
router.register('delete-complaint', DeleteComplaintsAndGrievancesViewset)
router.register('get-all-complaints-and-grievances', AllComplaintsAndGrievancesViewset)
router.register('get-user-complaints-and-grievances',
                UserComplaintsAndGrievancesViewset)
router.register('approve-complaints-and-grievances', ApproveComplaintsAndGrievancesViewset)
router.register('solution-status-complaints-and-grievances',
                SolutionStatusComplaintsAndGrievancesViewset)
router.register('update-complaints-and-grievances',
                UpdateComplaintsAndGrievancesViewset)

urlpatterns = [
    path('', include(router.urls))
]
