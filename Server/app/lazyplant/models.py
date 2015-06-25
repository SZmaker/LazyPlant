from django.db import models

# Create your models here.
class IoTRecord(models.Model):
    class Meta:
        verbose_name = 'IoT Record'
        verbose_name_plural = 'IoT Records'

    co2 = models.FloatField(null=True, blank=True)
    o2 = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="iotimages")
    timestamp = models.DateTimeField(null=True, blank=True)

