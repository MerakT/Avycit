from django.urls import path
from .views import *

urlpatterns = [
    path('raw/', RawProblemList.as_view(), name='raw-problem-list'),
    path('raw/<int:pk>/', RawProblemDetail.as_view(), name='raw-problem-detail'),
    path('clean/', CleanProblemList.as_view(), name='clean-problem-list'),
    path('clean/<int:pk>/', CleanProblemDetail.as_view(), name='clean-problem-detail'),
]
