from django.urls import path, include
from rest_framework import routers

from events.views import *

router = routers.DefaultRouter()

router.register('events', EventsViewset)
router.register('limited-events', LimitEventsViewset)
router.register('update-event', UpdateEventViewset)
router.register('delete-event', DeleteEventViewset)
router.register('news', NewsViewset)
router.register('limited-news', LimitNewsViewset)
router.register('update-news', UpdateNewsViewset)
router.register('delete-news', DeleteNewsViewset)

urlpatterns = [
    path('', include(router.urls))
]
