from django.db import models

from Users.models import Usuario, ProgAcad

RAW_STATUTES = [
    ('en revision', 'En revisión'),
    ('rechazado', 'Rechazado'),
    ('publicado', 'Publicado'),
]

STATUS_CHOICES = [
    ('tomado', 'Tomado'),
    ('abandonado', 'Abandonado'),
    ('finalizado', 'Finalizado'),
]

class RawProblem(models.Model):
    applicant = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    sector = models.CharField(max_length=150)
    institution_type = models.CharField(max_length=150)
    institution_name = models.CharField(max_length=150)
    description = models.TextField()
    file_1 = models.FileField(upload_to='problems/', blank=True, null=True)
    file_2 = models.FileField(upload_to='problems/', blank=True, null=True)
    file_3 = models.FileField(upload_to='problems/', blank=True, null=True)
    file_4 = models.FileField(upload_to='problems/', blank=True, null=True)
    raw_status = models.CharField(
        max_length=12,
        choices=RAW_STATUTES,
        default='en revision',
    )
    is_supported = models.BooleanField(default=False)
    observation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class CleanProblem(models.Model):
    raw_problem = models.ForeignKey(RawProblem, on_delete=models.CASCADE)
    clean_title = models.CharField(max_length=150)
    clean_description = models.TextField()
    clean_sector = models.CharField(max_length=150)
    career_1 = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, related_name='career_1')
    career_2 = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, related_name='career_2', blank=True, null=True)
    career_3 = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, related_name='career_3', blank=True, null=True)
    economic_support = models.IntegerField(default=0)
    social_support = models.IntegerField(default=0)
    enviromental_support = models.IntegerField(default=0)
    importancy = models.IntegerField(default=0)

    def __str__(self):
        return self.raw_problem.title
    
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