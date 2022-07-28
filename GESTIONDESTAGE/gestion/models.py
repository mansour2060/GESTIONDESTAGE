from django.db import models
from django.core.validators import FileExtensionValidator

class Stageir(models.Model):
    name=models.CharField(max_length=150,default="")
    prenom=models.CharField(max_length=150,default="")
    email=models.CharField(max_length=150,default="")
    service=models.CharField(max_length=120)
    debutstage=models.DateField()
    fintage=models.DateField()
    sexe=models.CharField(max_length=14)
    cv=models.FileField(validators=[ FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'ppt', 'xlsx'])])
    statu=models.CharField(max_length=100, default="")
class gestion(models.Model):
    name=models.CharField(max_length=150,default="")
    nameMaître =models.CharField(max_length=150,default="")
    Assiduité=models.CharField(max_length=150,default="")
    Option=models.CharField(max_length=150,default="")
    Adresse=models.CharField(max_length=150,default="")
    Période=models.CharField(max_length=150,default="")
    Initiative=models.CharField(max_length=150,default="")
    Communication=models.CharField(max_length=150,default="")
    Esprit =models.CharField(max_length=150,default="")
    Connaissances =models.CharField(max_length=150,default="")
    Total =models.CharField(max_length=150,default="")
    Observations  =models.CharField(max_length=1500,default="")
    number = models.BigIntegerField(default=0)
    statu=models.CharField(max_length=150,default="")





# Create your models here.
