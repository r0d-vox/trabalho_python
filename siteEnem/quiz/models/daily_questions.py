
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField

# Modelo de Alternativas
class Alternativa(models.Model):
    texto = models.TextField("Texto da Alternativa")
    correta = models.BooleanField("É Correta?", default=False)
    pergunta = models.ForeignKey(
        "PerguntaDiaria",
        related_name="alternativas",
        on_delete=models.CASCADE
    )

    panels = [
        FieldPanel("texto"),
        FieldPanel("correta"),
    ]

    def __str__(self):
        return f"{self.texto} ({'Correta' if self.correta else 'Errada'})"

# Modelo de Perguntas Diárias
class PerguntaDiaria(Page):
    texto_pergunta = models.TextField("Texto da Pergunta")
    explicacao = models.TextField("Explicação da Resposta Correta")

    content_panels = Page.content_panels + [
        FieldPanel('texto_pergunta'),
        FieldPanel('explicacao'),
        InlinePanel('alternativas', label="Alternativas"),
    ]

    api_fields = [
        APIField('texto_pergunta'),
        APIField('explicacao'),
        APIField('alternativas'),
    ]

class PaginaPerguntasDiarias(Page):
    texto_intro = models.TextField("Texto de Introdução", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('texto_intro'),
    ]

    def get_context(self, request):
        contexto = super().get_context(request)
        pergunta_diaria = PerguntaDiaria.objects.order_by('?').first()  # Seleciona uma pergunta aleatória
        contexto['pergunta_diaria'] = pergunta_diaria
        return contexto
