from django.db import models
from django.utils import timezone

from Users.models import Usuario

class Noti(models.Model):
    subject = models.CharField(max_length=150)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    sent_to = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='sent_to')
    sent_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='sent_by')
    seen = models.BooleanField(default=False)
    seen_timestamp = models.DateTimeField(blank=True, null=True)
    answered = models.BooleanField(default=False, blank=True, null=True)
    answered_timestamp = models.DateTimeField(blank=True, null=True)
    noti_number = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.seen:
            self.seen_timestamp = timezone.now()
        if self.answered:
            self.answered_timestamp = timezone.now()
        super(Noti, self).save(*args, **kwargs)