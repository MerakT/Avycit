from django.urls import path
from .views import mark_as_seen, NotiList

urlpatterns = [
    path('noti/<int:noti_id>/seen/', mark_as_seen, name='mark_as_seen'),
    path('my_notis/', NotiList.as_view(), name='my_notis'),
]