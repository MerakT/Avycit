from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from Users.models import Usuario, ProgAcad

RAW_STATUTES = [
    ('en espera', 'En espera'),
    ('en revision', 'En revisión'),
    ('rechazado', 'Resuelto'),
    ('publicado', 'Publicado'),
]

STATUS_CHOICES = [
    ('tomado', 'Tomado'),
    ('abandonado', 'Abandonado'),
    ('finalizado', 'Finalizado'),
]
#problemas en bruto -son los problemas antes de ser curados(p-natural)
class RawProblem(models.Model):
    # User Data
    applicant = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    # Contact Data
    email_contact = models.EmailField(default='1')
    phone_contact = models.CharField(max_length=15, default='1')
    institution_type = models.CharField(max_length=150, default=None, blank=True, null=True)
    institution_name = models.CharField(max_length=150, default=None, blank=True, null=True)
    ruc_contact = models.CharField(max_length=12, default=None, blank=True, null=True)
    razon_social_contact = models.TextField(default=None, blank=True, null=True)
    address_contact = models.TextField(default=None, blank=True, null=True)

    # Problem Data
    title = models.CharField(max_length=150)
    description = models.TextField()
    file_1 = models.FileField(upload_to='problems/', blank=True, null=True)
    file_2 = models.FileField(upload_to='problems/', blank=True, null=True)
    file_3 = models.FileField(upload_to='problems/', blank=True, null=True)
    file_4 = models.FileField(upload_to='problems/', blank=True, null=True)

    # Status Data
    raw_status = models.CharField(
        max_length=12,
        choices=RAW_STATUTES,
        default='en espera',
    )
    is_supported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Review Data
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
#problemas curados  
class CleanProblem(models.Model):
    raw_problem = models.ForeignKey(RawProblem, on_delete=models.CASCADE)
    clean_title = models.CharField(max_length=150)
    clean_description = models.TextField()
    clean_sector = models.CharField(max_length=150)
    #carrera del curador - P.A
    career_1 = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, related_name='career_1')
    career_2 = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, related_name='career_2', blank=True, null=True)
    career_3 = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, related_name='career_3', blank=True, null=True)
    economic_support = models.IntegerField(default=0)
    social_support = models.IntegerField(default=0)
    enviromental_support = models.IntegerField(default=0)
    importancy = models.IntegerField(default=0)
   # nuevos cambios 
   #campos para tipo de respuesta solución
    tipo_solucion=models.CharField(max_length=150,null=True)
    soluc_description=models.TextField(null=True)
    #campos para tipo de respuesta-trabajo de curso
    tec_type = models.CharField(max_length=150,null=True) #tipo de tecnologia
    tra_adonde = models.CharField(max_length=150,null=True) #a donde se dirige la solucion
    tra_quienes = models.CharField(max_length=150,null=True) #a quienes va dirigido
    tra_problema = models.CharField(max_length=150,null=True) #cual es el problema
    tra_causas = models.TextField(null=True) #causas
    tra_consecuencias = models.TextField(null=True) #consecuencias
    tra_aportes = models.TextField(null=True) #aportes
    #campos para tipo de respuesta-investigación
    titulo_pcca = models.CharField(max_length=150,null=True) #titulo del proyecto
    problema = models.TextField(null=True) #problema
    variable1 = models.CharField(max_length=150,null=True) #variable 1
    variable2 = models.CharField(max_length=150,null=True) #variable 2
    #campos para tipo de respuesta _ proyecto
    nom_proyect = models.CharField(max_length=150,null=True) #nombre del proyecto
    preparado_por = models.CharField(max_length=150,null=True) #preparado por
    justificacion = models.TextField(null=True) #justificacion
    objetivos = models.TextField(null=True) #objetivos
    alcance = models.TextField(null=True) #alcance
    descripcion_pro = models.TextField(null=True) #descripcion del proyecto
    
    
    # Override the save method to calculate the importancy and refuse creation if there is a raw problem associated with another clean problem
    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                clean_problem_with_raw_associated = CleanProblem.objects.get(raw_problem=self.raw_problem)
                raise Exception('There is already a clean problem associated with this raw problem')
            except ObjectDoesNotExist:
                self.importancy = int((self.economic_support + self.social_support + self.enviromental_support) / 3)
        super(CleanProblem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.clean_title} - Basado en => " {self.raw_problem.title}"'
    
class TakenProblems(models.Model):
    problem = models.ForeignKey(CleanProblem, on_delete=models.CASCADE)
    student = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='tomado',
    )
    
    def __str__(self):
        return self.problem.title + ' - ' + self.student.first_name + ' ' + self.student.last_name
    
#-------------------------------------- VRI DATA ------------------------------------
class VRIProblemData(models.Model):
    raw_problem = models.ForeignKey(RawProblem, on_delete=models.CASCADE)
    vri_title = models.CharField(max_length=150)
    economic_fond = models.IntegerField(default=0)
    is_viable = models.BooleanField(default=False)