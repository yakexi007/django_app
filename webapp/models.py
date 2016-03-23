from django.db import models

# Create your models here.

class history_data(models.Model):
    datetime = models.CharField(max_length=20)
    person = models.CharField(max_length=20)
    types = models.CharField(max_length=20)
    reason = models.CharField(max_length=100)
    path = models.CharField(max_length=50000)
    result = models.CharField(max_length=50000)

class UploadFile(models.Model):
    username=models.CharField(max_length=50)
    uploadfile=models.FileField(upload_to='/upload/') 
    
    def __unicode__(self):
        return username
