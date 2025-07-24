from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('chat_home')
    return redirect('welcome')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect),
    path('', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
