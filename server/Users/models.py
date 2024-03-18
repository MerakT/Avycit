from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

REGISTRATION_CHOICES = [
    ('email', 'Email'),
    ('google', 'Google'),
]

ROLE_CHOICES = [
    # Banco de Problemas
    ('p_natural', 'Natural'),
    ('emprendedor', 'Emprendedor'),
    ('empresa', 'Empresa'),
    ('ong', 'ONG'),
    ('gobierno', 'Gobierno'),
    ('admin', 'Admin'),
    ('vri', 'Vri'),

    # UDH
    ('tesista', 'Tesista'),
    ('asesor', 'Asesor'),
    ('jurado', 'Jurado'),
    ('coordinador', 'Coordinador'),
    ('sec_prog', 'Sec. Programa'),
    ('sec_fac', 'Sec. Facultad'),
]

class Facultad(models.Model):
    name = models.CharField(max_length=150)
    dean = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class ProgAcad(models.Model):
    name = models.CharField(max_length=150)
    faculty = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    coord = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
class Usuario(AbstractUser):
    # General Fields
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='tesista'
    )

    # UDH Fields
    career = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=12, unique=True, blank=True, null=True)
    grado = models.CharField(max_length=150, blank=True, null=True)
    signature_photo = models.ImageField(upload_to='signatures/', blank=True, null=True)

    # Banco de Problemas Fields
    dni = models.CharField(max_length=8, blank=True, null=True)
    ruc = models.CharField(max_length=11, blank=True, null=True) # EMPRESA
    razon_social = models.CharField(max_length=150, blank=True, null=True) # EMPRESA
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    can_finance = models.BooleanField(default=False, blank=True, null=True)
    charge = models.CharField(max_length=50, blank=True, null=True) # EMPRESA
    area = models.CharField(max_length=100, blank=True, null=True) # EMPRESA
    registration_method = models.CharField(
        max_length=20, 
        choices=REGISTRATION_CHOICES, 
        default='email'
    )

    objects = UsuarioManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)