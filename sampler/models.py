from django.db import models

# Create your models here.
class ExcelDocument(models.Model):
    docFile = models.FileField(upload_to='documents')