from django.db import models


class CpuData(models.Model):
    id = models.AutoField(primary_key=True)
    percent = models.FloatField()
    dateTime = models.DateTimeField()

    class Meta:
        db_table = "procLoadHistory"
        verbose_name_plural = 'Cpu Load Data'

    def __str__(self):
        return f'{self.id} {self.percent} {self.dateTime}'
