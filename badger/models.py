import os

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Model3d(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='models', blank=True, null=True, verbose_name='Image')
    views = models.IntegerField(default=0, verbose_name='Nombre de vues')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='models')

    class Meta:
        db_table = 'model3D'
        verbose_name = 'Modèle 3D'
        verbose_name_plural = 'Modèles 3D'

    def __str__(self):
        return self.name

class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='badges')

    class Meta:
        db_table = 'badge'
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='users')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_badge'
        verbose_name = 'UserBadge'
        verbose_name_plural = 'UserBadges'

    def __str__(self):
        return self.user.username + ' - ' + self.badge.name
