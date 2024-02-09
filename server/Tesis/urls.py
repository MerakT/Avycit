from django.urls import path, include
from .views import *


urlpatterns = [
    path('tesislist', TesisList.as_view()),
    path('tesisdetail/<int:pk>', TesisDetail.as_view()),
]