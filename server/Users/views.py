from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from .models import ProgAcad
from .serializers import ProgAcadSerializer

class ProgAcadList(ListCreateAPIView):
    queryset = ProgAcad.objects.all()
    serializer_class = ProgAcadSerializer
