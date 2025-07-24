from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chatapp.views import root_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_view, name='root'),
    path('accounts/', include('accounts.urls')),
    path('', include('chatapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
