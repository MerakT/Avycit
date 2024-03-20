from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from django.conf import settings
from django.http import HttpResponseRedirect

from .models import ProgAcad
from .serializers import ProgAcadSerializer


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )

def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )

class ProgAcadList(ListCreateAPIView):
    queryset = ProgAcad.objects.all()
    serializer_class = ProgAcadSerializer
