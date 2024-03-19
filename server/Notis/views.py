from django.http import JsonResponse
from .models import Noti
from .serializers import NotiSerializer
from rest_framework.generics import ListAPIView

def mark_as_seen(request, noti_id):
    try:
        noti = Noti.objects.get(id=noti_id)
        noti.seen = True
        noti.save()
        return JsonResponse({'message': 'Notification marked as seen.'})
    except Noti.DoesNotExist:
        return JsonResponse({'error': 'Notification not found.'}, status=404)
    
class NotiList(ListAPIView):
    serializer_class = NotiSerializer

    def get_queryset(self):
        return Noti.objects.filter(sent_to=self.request.user).order_by('-sent_date')
