from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return '{0}/{1}'.format(instance.user.id, filename)

def user_thumbnail_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/thumbnails/<filename>
    return '{0}/{1}'.format(str(instance.user.id) + '/thumbnails', filename)


class Post(models.Model):
  class PostStatus(models.TextChoices):
    NEW = 'new', _('new')
    APPROVED = 'approved', _('approved')
    REJECTED = 'rejected', _('rejected')

  user = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name="post_user_id", to_field="id")
  added = models.DateTimeField(auto_now_add=True)
  media_file = models.FileField(upload_to=user_directory_path, blank=True)
  thumbnail = models.FileField(
      upload_to=user_thumbnail_directory_path, blank=True)
  title = models.CharField(_('title'), max_length=100, blank=True)
  description = models.TextField(_("description"), max_length=20000, blank=True)
  post_status = models.CharField(
      _('post status'), max_length=15, choices=PostStatus.choices, default=PostStatus.NEW)

  def __str__(self):
    return self.title


class PostComment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user", to_field="id")
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post", to_field="id")
  comment = models.TextField(_("comment"), max_length=20000, blank=True)
  added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.post


class ComplaintsAndGrievances(models.Model):
  class ComplaintsAndGrievancesStatus(models.TextChoices):
    NEW = 'new', _('new')
    APPROVED = 'approved', _('approved')
    REJECTED = 'rejected', _('rejected')
  class ComplaintsAndGrievancesSolutionStatus(models.TextChoices):
    UNSOLVED = 'unsolved', _('unsolved')
    SOLVED = 'solved', _('solved')

  user = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name="complaints_user_id", to_field="id")
  added = models.DateTimeField(auto_now_add=True)
  title = models.CharField(_('title'), max_length=100, blank=True)
  description = models.TextField(_("description"), max_length=20000, blank=True)
  status = models.CharField(
      _('complaints status'), max_length=15, choices=ComplaintsAndGrievancesStatus.choices, default=ComplaintsAndGrievancesStatus.NEW)
  solution_status = models.CharField(
      _('complaints solution status'), max_length=15, choices=ComplaintsAndGrievancesSolutionStatus.choices, default=ComplaintsAndGrievancesSolutionStatus.UNSOLVED)

  def __str__(self):
    return self.title
