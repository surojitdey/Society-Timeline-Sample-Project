import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings


def tnails(file):
   try:
      image = Image.open(file)
      img_width, img_height = image.size

      original_ratio = img_width/img_height
      given_ratio = settings.THUMBNAIL_SIZE[0]/settings.THUMBNAIL_SIZE[1]
      if(original_ratio == given_ratio):
        resize_width = settings.THUMBNAIL_SIZE[0]
        resize_height = settings.THUMBNAIL_SIZE[1]
      elif(original_ratio > given_ratio):
        resize_height = settings.THUMBNAIL_SIZE[1]
        resize_width = int(resize_height * original_ratio)
      else:
        resize_width = settings.THUMBNAIL_SIZE[0]
        resize_height = int(resize_width / original_ratio)
      
      
      image = image.resize((resize_width, resize_height), Image.ANTIALIAS)

      thumb_name, thumb_extension = os.path.splitext(file.name)
      thumb_extension = thumb_extension.lower()
      thumb_filename = thumb_name + '_thumb' + thumb_extension

      if thumb_extension in ['.jpg', '.jpeg']:
          FTYPE = 'JPEG'
      elif thumb_extension == '.gif':
          FTYPE = 'GIF'
      elif thumb_extension == '.png':
          FTYPE = 'PNG'
      else:
          return None, None, None    # Unrecognized file type
      
      return image, FTYPE, thumb_filename
   except IOError:
      return None, None, None

