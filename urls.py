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
    path('api/signup/',      views.signup,      name='signup'),
    path('api/login/',       views.login,       name='login'),
    path('api/place-order/', views.place_order, name='place_order'),
    path('api/my-orders/',   views.get_orders,  name='get_orders'),
]


from django.urls import path
from . import views



