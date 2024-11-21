from django.db import models
from wagtail.users.models import UserProfile
from .daily_questions import PerguntaDiaria

class ProgressoUsuario(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(PerguntaDiaria, on_delete=models.CASCADE)
    acertou = models.BooleanField()

    def __str__(self):
        return f"{self.usuario.user.username} - {'Acertou' if self.acertou else 'Errou'}"
