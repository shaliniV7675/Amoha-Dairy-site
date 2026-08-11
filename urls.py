from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.http import HttpResponse, Http404
import os

def serve_html(request, filename):
    """Serve any .html file from the Amoha frontend folder."""
    filepath = os.path.join(settings.FRONTEND_DIR, filename)
    if not os.path.exists(filepath):
        raise Http404(f"{filename} not found")
    with open(filepath, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='text/html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
     path('dashboard/', include('dashboard.urls')),

    # Serve frontend HTML pages: http://127.0.0.1:8000/login.html
    re_path(r'^(?P<filename>[\w\- ]+\.html)$', serve_html),
]
