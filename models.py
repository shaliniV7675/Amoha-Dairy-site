from django.db import models
class User(models.Model):
    full_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)

    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.email

# Create your models here.
