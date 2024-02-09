from django.db import models

from Users.models import Usuario

class Temas(models.Model):
    name = models.CharField(max_length=150)
    theory = models.TextField()

class Subtemas(models.Model):
    theme = models.ForeignKey(Temas, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    theory = models.TextField()

class Ejemplos(models.Model):
    subject = models.ForeignKey(Subtemas, on_delete=models.CASCADE)
    content = models.TextField()