from django.contrib import admin
from .models import Usuario, Facultad, ProgAcad

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Facultad)
admin.site.register(ProgAcad)