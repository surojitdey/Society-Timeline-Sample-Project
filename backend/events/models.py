from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


def events_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/events/<filename>
    return '{0}/{1}'.format('events', filename)

def events_thumbnail_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/events/thumbnail/<filename>
    return '{0}/{1}'.format('events/thumbnail/', filename)

def news_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/news/<filename>
    return '{0}/{1}'.format('news', filename)

def news_thumbnail_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/news/thumbnail/<filename>
    return '{0}/{1}'.format('news/thumbnail/', filename)


class Events(models.Model):
  class TimeConvention(models.TextChoices):
    AM = 'am', _('am')
    PM = 'pm', _('pm')

  title = models.CharField(_('title'), max_length=100, blank=False)
  description = models.TextField(_("description"), max_length=20000, blank=False)
  added = models.DateTimeField(auto_now_add=True)
  media_file = models.FileField(upload_to=events_directory_path, blank=True)
  thumbnail = models.FileField(
      upload_to=events_thumbnail_directory_path, blank=True)
  event_date = models.DateField(blank=False)
  event_time = models.CharField(_('event time'), max_length=2, blank=True, null=True)
  time_convention = models.CharField(
      _('time convention'), choices=TimeConvention.choices, max_length=2, blank=True, null=True)


class News(models.Model):
  title = models.CharField(_('title'), max_length=100, blank=False)
  description = models.TextField(_("description"), max_length=20000, blank=False)
  added = models.DateTimeField(auto_now_add=True)
  media_file = models.FileField(upload_to=news_directory_path, blank=True, null=True)
  thumbnail = models.FileField(
      upload_to=news_thumbnail_directory_path, blank=True)
