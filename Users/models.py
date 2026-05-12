from django.db import models

# Create your models here.
class UserRegisterModel(models.Model):
    Name = models.CharField(max_length=30)
    Username = models.CharField(max_length=30)
    Password= models.CharField(max_length=30)
    Email = models.CharField(max_length=30)
    Phone_No = models.CharField(max_length=10)
    Locality = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Address = models.CharField(max_length=30)
    status = models.CharField(max_length=10)
    def __str__(self):
        return self.Name