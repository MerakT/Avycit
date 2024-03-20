from django.contrib import admin
from django.urls import path, include

# for media files
from django.conf import settings
from django.conf.urls.static import static

# for various types of data
from Users.views import ProgAcadList

urlpatterns = [
    # Apps Related
    path('admin/', admin.site.urls),
    path('accounts/' ,include('Users.urls')),
    path('tesis/', include('Tesis.urls')),
    path('problems/', include('Problems.urls')),
    path('notis/', include('Notis.urls')),

    # Data Related
    path('data/careers/', ProgAcadList.as_view(), name='careers-list'), # For careers list
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
