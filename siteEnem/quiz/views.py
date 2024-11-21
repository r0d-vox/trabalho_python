from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models.daily_questions import PerguntaDiaria, Alternativa
from django.views.decorators.csrf import csrf_exempt
from wagtail.models import Page
from django.utils.text import slugify
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PerguntaDiaria, Alternativa
import json
from django.conf import settings
import os
import random


def pergunta_do_dia(request):
    # Define the path to the JSON file
    json_file_path = os.path.join(settings.BASE_DIR, 'quiz', 'fixtures', 'perguntas.json')

    # Check if the file exists
    if not os.path.exists(json_file_path):
        return render(request, 'home/perguntas_diarias.html', {
            'error': 'O arquivo de perguntas não foi encontrado.'
        })

    # Read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return render(request, 'home/perguntas_diarias.html', {
            'error': 'Erro ao carregar as perguntas do arquivo.'
        })

    # Extract questions and alternatives
    perguntas = [item for item in data if item['model'] == 'quiz.PerguntaDiaria']
    alternativas = [item for item in data if item['model'] == 'quiz.Alternativa']

    # Randomly select a question
    if perguntas:
        pergunta_selecionada = random.choice(perguntas)

        # Find alternatives for the selected question
        pergunta_alternativas = [
            alt for alt in alternativas
            if alt['fields']['pergunta'] == pergunta_selecionada['pk']
        ]

        # Prepare the question dictionary to match the template expectations
        pergunta_diaria = {
            'id': pergunta_selecionada['pk'],
            'texto_pergunta': pergunta_selecionada['fields']['texto_pergunta'],
            'explicacao': pergunta_selecionada['fields'].get('explicacao', ''),
            'alternativas': [
                {
                    'texto': alt['fields']['texto'],
                    'correta': alt['fields']['correta']
                } for alt in pergunta_alternativas
            ]
        }

        return render(request, 'home/perguntas_diarias.html', {
            'pergunta_diaria': pergunta_diaria,
        })

    return render(request, 'home/perguntas_diarias.html', {
        'error': 'Nenhuma pergunta encontrada no arquivo.'
    })

@csrf_exempt
def submit_resposta(request):
    if request.method == "POST":
        # Load the JSON data
        json_file_path = os.path.join(settings.BASE_DIR, 'quiz', 'fixtures', 'perguntas.json')
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get the submitted answer
        resposta_usuario = request.POST.get('resposta_usuario')

        # Find the corresponding question and alternatives
        for item in data:
            if item['model'] == 'quiz.Alternativa' and item['fields']['texto'] == resposta_usuario:
                # Check if this alternative is correct
                if item['fields']['correta']:
                    # Find the question's explanation
                    pergunta = next((q for q in data if q['model'] == 'quiz.PerguntaDiaria' and q['pk'] == item['fields']['pergunta']), None)
                    explicacao = pergunta['fields'].get('explicacao', '') if pergunta else ''
                    return JsonResponse({'resultado': 'Correto!', 'explicacao': explicacao})
                else:
                    # Find the question's explanation
                    pergunta = next((q for q in data if q['model'] == 'quiz.PerguntaDiaria' and q['pk'] == item['fields']['pergunta']), None)
                    explicacao = pergunta['fields'].get('explicacao', '') if pergunta else ''
                    return JsonResponse({'resultado': 'Incorreto!', 'explicacao': explicacao})

        return JsonResponse({'erro': 'Resposta inválida'})
    return JsonResponse({'erro': 'Método inválido'})


@csrf_exempt
def create_pergunta(request):
    if request.method == "POST":
        texto_pergunta = request.POST.get('texto_pergunta')
        explicacao = request.POST.get('explicacao')
        alternativas_data = request.POST.getlist('alternativas')

        # Ensure you are assigning the PerguntaDiaria to a valid parent page
        parent_page = Page.objects.get(id=1)  # Replace 1 with the ID of your parent page (root page is typically ID=1)

        # Create the PerguntaDiaria page
        page = PerguntaDiaria(
            title=texto_pergunta,  # Use the text of the question as the title
            slug=slugify(texto_pergunta),  # Generate the slug from the question text
            texto_pergunta=texto_pergunta,
            explicacao=explicacao,
        )

        # Set the parent page for this page
        page.parent = parent_page  # This is how you assign the parent page

        # Save the page to populate path and depth
        page.save()

        # Now, create alternatives
        for alternativa_data in alternativas_data:
            texto = alternativa_data.get('texto')
            correta = alternativa_data.get('correta') == 'on'
            Alternativa.objects.create(pergunta=page, texto=texto, correta=correta)

        # Redirect to the question of the day page (or any other page you want)
        return redirect('pergunta_do_dia')  # Change this to your desired redirect page
    return JsonResponse({'erro': 'Método inválido'})