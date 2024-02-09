from django.db import models

from Users.models import Usuario
from Tesis.models import Tesis

#---------------------------- UTILIDADES ----------------------------
# Para el path de los archivos
def get_upload_path(instance, filename):
    return f'Docs/{instance.doc_related.type_doc}/{instance.doc_related.tesis.student}/{instance.type_file}/{filename}'

# FIRMA DIGITAL
class FirmaDigital(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    signature_token = models.CharField(max_length=150)

#---------------------------- Documentos Varios ------------------------------
class DocVario(models.Model):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE, related_name="tesis_doc",blank=True, null=True)
    advisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='advisor_doc', blank=True, null=True)
    judge_1 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='judge_1_doc', blank=True, null=True)
    judge_2 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='judge_2_doc', blank=True, null=True)
    judge_3 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='judge_3_doc', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type_doc = models.CharField(max_length=150)
    doc_number = models.IntegerField()
    sign = models.ForeignKey(FirmaDigital, on_delete=models.CASCADE)

class ArchivosDoc(models.Model):
    doc_related = models.ForeignKey(DocVario, on_delete=models.CASCADE, related_name="tesis_doc",blank=True, null=True)
    type_file = models.CharField(max_length=150)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_upload_path)

# HORARIOS Y COSAS DE JURADOS
class DetalleSustentacion(models.Model):
    doc_detalle = models.ForeignKey(DocVario, on_delete=models.CASCADE)
    day = models.DateField()
    hour = models.TimeField()
    classroom = models.CharField(max_length=50)

class TesisFinalizada(models.Model):
    tesista = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    final_doc = models.FileField(upload_to='Repositorio/Finalizados/')


