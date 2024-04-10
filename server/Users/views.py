from rest_framework import authentication, permissions
from rest_framework.generics import ListCreateAPIView
from django.conf import settings
from django.http import HttpResponseRedirect

from .models import ProgAcad
from .serializers import CareerSerializer
from Tesis.views import OnlyCoordinador


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )

def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )

class ProgAcadList(ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = ProgAcad.objects.all()
    serializer_class = CareerSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [OnlyCoordinador()]
        return [permissions.IsAuthenticated]
    