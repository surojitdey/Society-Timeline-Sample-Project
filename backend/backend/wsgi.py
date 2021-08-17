import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

project_folder = os.path.dirname(os.path.abspath('../'+__file__))
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
