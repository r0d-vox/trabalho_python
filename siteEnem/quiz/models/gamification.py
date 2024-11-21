from django.db import models
from wagtail.users.models import UserProfile

class Gamification(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)
    medalhas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.usuario.user.username} - Pontos: {self.pontos}"
