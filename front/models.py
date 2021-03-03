from django.db import models

# Create your models here.


class PosicionFront(models.Model):
    posicion = models.PositiveSmallIntegerField()
    user = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'posicion_front'
        constraints = [
            models.UniqueConstraint(fields=['posicion', 'user'], name='posicion_user')
        ]
