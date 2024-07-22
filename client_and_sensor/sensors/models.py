from django.db import models

# Create your models here.

class Sensor(models.Model):
    qr_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
