import os
from django.core.wsgi import get_wsgi_application

# Get the port from the environment variable or default to 8000
port = int(os.environ.get('PORT', 8000))

# Start the Gunicorn server
bind = f'0.0.0.0:{port}'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskforce.settings')

application = get_wsgi_application()
