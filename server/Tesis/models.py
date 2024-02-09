from django.db import models

from Users.models import Usuario
from Problems.models import CleanProblem

#---------------------------- PARA LA FICHA PRELIMINAR ----------------------------
CREATED_OPTIONS = [
    ('banco', 'Banco de Problemas'),
    ('propio', 'Propio')
]

class FichaPreliminar(models.Model):
    problem_description = models.TextField()
    title_ficha = models.CharField(max_length=150)
    obj_gen = models.TextField()
    hipo_gen = models.TextField()
    bank_problem = models.ForeignKey(CleanProblem, on_delete=models.CASCADE, blank=True, null=True)
    created_option = models.CharField(
        max_length=6,
        choices=CREATED_OPTIONS,
        default='propio',
    )
    student_ficha  = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Variables(models.Model):
    ficha = models.ForeignKey(FichaPreliminar, on_delete=models.CASCADE)
    name_variable = models.CharField(max_length=150)
    type_variable = models.CharField(max_length=150)
    justification = models.TextField()
    
class ObjetivosEsp(models.Model):
    ficha = models.ForeignKey(FichaPreliminar, on_delete=models.CASCADE)
    description = models.TextField()

class HipotesisEsp(models.Model):
    ficha = models.ForeignKey(FichaPreliminar, on_delete=models.CASCADE)
    description = models.TextField()

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
    ficha = models.ForeignKey(FichaPreliminar, on_delete=models.CASCADE)
    linea = models.CharField(max_length=150)
    nivel = models.CharField(max_length=150)
    sub_linea = models.CharField(max_length=150)
    sub_sub_linea = models.CharField(max_length=150)
    producto = models.CharField(max_length=150)
    finalidad = models.CharField(max_length=150)
