from django.db import models
from wagtail.users.models import UserProfile
from .daily_questions import PerguntaDiaria

class ForumDiscussao(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(PerguntaDiaria, on_delete=models.CASCADE)
    comentario = models.TextField("Comentário")

    def __str__(self):
        return f"Discussão de {self.usuario.user.username} - {self.pergunta.texto_pergunta[:50]}"
