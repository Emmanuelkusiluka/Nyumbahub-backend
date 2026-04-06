from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test', views.test, name='test'),
    path('api/auth/', include('accounts.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/reports/', include('reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
