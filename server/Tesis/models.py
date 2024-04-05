from django.db import models

from Users.models import Usuario, ProgAcad
from Problems.models import RawProblem

#---------------------------- PARA LA FICHA PRELIMINAR ----------------------------
CREATED_OPTIONS = [
    ('banco', 'Banco de Problemas'),
    ('propio', 'Propio')
]

STATUS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aceptado', 'Aceptado'),
]

class PropuestaTesis(models.Model):
    # User Data
    creator = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Propuesta Data
    career = models.ForeignKey(ProgAcad, on_delete=models.CASCADE)
    propuesta_raw = models.ForeignKey(RawProblem, on_delete=models.CASCADE)
    donde = models.CharField(max_length=300)
    quienes = models.CharField(max_length=300)
    problema = models.CharField(max_length=300)
    # Lote 1
    propuesta_title = models.CharField(max_length=150)
    propuesta_problem = models.TextField()
    propuesta_objetive = models.TextField()
    propuesta_hipotesis = models.TextField()
    # Lote 2
    investigation_type = models.CharField(max_length=50)
    focus = models.CharField(max_length=50)
    level = models.CharField(max_length=50)  
    design = models.CharField(max_length=50)

# Lote 1
class Causas(models.Model):
    propuesta = models.ForeignKey(PropuestaTesis, on_delete=models.CASCADE, default=1)
    description = models.TextField()

class Consecuencias(models.Model):
    propuesta = models.ForeignKey(PropuestaTesis, on_delete=models.CASCADE, default=1)
    description = models.TextField()

class Aportes(models.Model):
    propuesta = models.ForeignKey(PropuestaTesis, on_delete=models.CASCADE, default=1)
    description = models.TextField()

# Lote 2
class Variables(models.Model):
    propuesta = models.ForeignKey(PropuestaTesis, on_delete=models.CASCADE, default=1)
    name_variable = models.CharField(max_length=150)
    type_variable = models.CharField(max_length=150)
    justification = models.TextField()
    
class ObjetivosEsp(models.Model):
    propuesta = models.ForeignKey(PropuestaTesis, on_delete=models.CASCADE, default=1)
    description = models.TextField()

class HipotesisEsp(models.Model):
    propuesta = models.ForeignKey(PropuestaTesis, on_delete=models.CASCADE, default=1)
    description = models.TextField()

class Postulaciones(models.Model):
    propuesta = models.ForeignKey(PropuestaTesis, on_delete=models.CASCADE)
    tesista = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=12,
        choices= STATUS_CHOICES,
        default='pendiente',
        )

#----------------------------- PARA LA TESIS ---------------------------------------------
STATUS_CHOICES = [
    ('proyecto', 'Proyecto'),
    ('ejecucion', 'En Ejecucion'),
    ('borrador', 'Borrador'),
    ('finalizado', 'Finalizado')
]

class Tesis(models.Model):
    title_tesis = models.CharField(max_length=150)
    sector_tesis = models.CharField(max_length=150)
    student = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='student_tesis')
    docs_link = models.URLField(blank=True, null=True) 
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices= STATUS_CHOICES,
        default='proyecto',
        )

class Observaciones(models.Model):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    written_by = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    written_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    file = models.FileField(upload_to='Observaciones/', blank=True, null=True)

#------------------------------- UTILIDADES MODELOS ------------------------------
class Metodologia(models.Model):
    ficha = models.ForeignKey(PropuestaTesis, on_delete=models.CASCADE)
    linea = models.CharField(max_length=150)
    nivel = models.CharField(max_length=150)
    sub_linea = models.CharField(max_length=150)
    sub_sub_linea = models.CharField(max_length=150)
    producto = models.CharField(max_length=150)
    finalidad = models.CharField(max_length=150)
