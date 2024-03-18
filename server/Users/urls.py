from django.urls import path, include
from .views import ProgAcadList

urlpatterns = [
    path('auth' ,include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('data/careers/', ProgAcadList.as_view()),
]