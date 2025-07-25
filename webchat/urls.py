from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from chatapp.views import root_view
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_view, name='root'),
    path('accounts/', include('accounts.urls')),
    path('', include('chatapp.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

