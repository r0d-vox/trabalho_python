# quiz/urls.py
from django.urls import path
from .views import pergunta_do_dia, submit_resposta, create_pergunta

urlpatterns = [
    path('perguntas/', pergunta_do_dia, name='pergunta_do_dia'),
    path('submit-resposta/', submit_resposta, name='submit_resposta'),
    path('create-pergunta/', create_pergunta, name='create_pergunta'),
]
