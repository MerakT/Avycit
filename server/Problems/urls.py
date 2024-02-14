from django.urls import path
from .views import *

urlpatterns = [
    path('rawproblems/', RawProblemList.as_view(), name='raw-problem-list'),
    path('rawproblems/<int:pk>/', RawProblemDetail.as_view(), name='raw-problem-detail'),
    path('cleanproblems/', CleanProblemList.as_view(), name='clean-problem-list'),
]
