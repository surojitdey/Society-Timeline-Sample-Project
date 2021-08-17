from django.db.models.signals import pre_save, post_init, post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
from posts.models import Post
from helpers.image import tnails


@receiver(pre_save, sender=Post)
def save_thumbnails(sender, instance, *args, **kwargs):
  if instance.media_file == 'null':
    instance.media_file = None
  if instance.media_file:
    image, FTYPE, thumb_filename = tnails(instance.media_file)
    if image is not None:
      temp_thumb = BytesIO()
      image.save(temp_thumb, FTYPE)
      temp_thumb.seek(0)
      
      # set save=False, otherwise it will run in an infinite loop
      instance.thumbnail.save(thumb_filename, ContentFile(
          temp_thumb.read()), save=False)
      temp_thumb.close()
