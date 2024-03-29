from django.urls import path
from .views import *


urlpatterns = [
    path('propuestas/', PropuestaTesisList.as_view(), name='propuestas'),
    path('propuestas/<int:pk>/', PropuestaTesisDetail.as_view(), name='propuesta'),
    path('postulaciones/', PostulacionesList.as_view(), name='postulaciones'),
    path('postulaciones/<int:pk>/', PostulacionesDetail.as_view(), name='postulacion'),
]