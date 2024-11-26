from django.shortcuts import render, get_object_or_404, redirect
from .models import FilmeSerie
from .forms import FilmeSerieForm
import logging
from django.http import JsonResponse
import requests
import random



logger = logging.getLogger(__name__)

def criar_filme_serie(request):
    if request.method == 'POST':
        logger.debug(f"Arquivos recebidos: {request.FILES}")
        form = FilmeSerieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_filmes_series')  # Redireciona para a listagem
        else:
            logger.debug(f"Erros no formulário: {form.errors}")
    else:
        form = FilmeSerieForm()
    return render(request, 'cadastro/criar_filme_serie.html', {'form': form})


def listar_filmes_series(request):
    filmes_series = FilmeSerie.objects.all()  # Obtém todos os filmes e séries
    return render(request, 'cadastro/listar_filmes_series.html', {'filmes_series': filmes_series})


def editar_filme_serie(request, id):
    filme_serie = get_object_or_404(FilmeSerie, id=id)
    
    if request.method == 'POST':
        form = FilmeSerieForm(request.POST, request.FILES, instance=filme_serie)
        if form.is_valid():
            form.save()
            return redirect('listar_filmes_series')  # Redireciona para a página de listagem após editar
    else:
        form = FilmeSerieForm(instance=filme_serie)
    
    return render(request, 'cadastro/editar_filme_serie.html', {'filme_serie': filme_serie})


def excluir_filme_serie(request, id):
    filme_serie = get_object_or_404(FilmeSerie, id=id)
    filme_serie.delete()
    return redirect('listar_filmes_series')  # Redireciona para a lista de filmes e séries

def listar_assistidos(request):
    assistidos = FilmeSerie.objects.filter(assistido=True)
    return render(request, 'cadastro/listar_assistidos.html', {'filmes_series': assistidos})

def listar_nao_assistidos(request):
    nao_assistidos = FilmeSerie.objects.filter(assistido=False)
    return render(request, 'cadastro/listar_nao_assistidos.html', {'filmes_series': nao_assistidos})

def marcar_assistido(request, id):
    filme = get_object_or_404(FilmeSerie, id=id)
    filme.assistido = True
    filme.save()
    return redirect('listar_nao_assistidos')
def alternar_status(request, filme_id):
    filme = get_object_or_404(FilmeSerie, id=filme_id)
    filme.assistido = not filme.assistido  # Alterna o status
    filme.save()
    return redirect('listar_filmes_series')
def obter_sugestao_filme(request):
    try:
        # Defina a chave da API
        api_key = '1a39e23e'

        # # Lista de palavras-chave para sugestões variadas
        # keywords = ['action', 'comedy', 'drama', 'romance', 'adventure']
        # # Escolhe aleatoriamente uma palavra-chave
        # # Realiza várias requisições para filmes aleatórios
        # for _ in range(5):  # Ajuste esse número para a quantidade de sugestões que você deseja
        #     keyword = random.choice(keywords)  # Escolhe um título aleatório
        #     url = f"http://www.omdbapi.com/?s={keyword}&apikey={api_key}"
        
        
        titulos = [
            'Gladiator', 'Jurassic Park', 'Star Wars: A New Hope', 'The Lion King', 'Harry Potter and the Sorcerer\'s Stone',
            'Fight Club', 'The Lord of the Rings: The Fellowship of the Ring', 'The Social Network', 'Spider-Man: No Way Home',
            'Black Panther', 'Avatar', 'The Silence of the Lambs', 'Coco', 'The Grand Budapest Hotel', 'Inglourious Basterds',
            'The Wolf of Wall Street', 'Whiplash', 'Parasite', 'A Quiet Place', 'Django Unchained'
        ]
        
        filmes_sugeridos = []
        
        # Realiza várias requisições para filmes aleatórios
        for _ in range(2):  # Ajuste esse número para a quantidade de sugestões que você deseja
            titulo = random.choice(titulos)  # Escolhe um título aleatório
            url = f"http://www.omdbapi.com/?t={titulo}&apikey={api_key}"
            

            # Faz a requisição à API
            response = requests.get(url)
            response.raise_for_status()

            if response.status_code == 200:
                dados_filme = response.json()
                if dados_filme.get('Response') == 'True':
                    filmes_sugeridos.append(dados_filme)
        
        if filmes_sugeridos:
            return render(request, 'cadastro/sugestao_filme.html', {'filmes': filmes_sugeridos})
        else:
            return render(request, 'cadastro/sugestao_filme.html', {'erro': 'Nenhuma sugestão encontrada.'})
    
    except requests.exceptions.RequestException as e:
        return render(request, 'cadastro/sugestao_filme.html', {'erro': f'Erro ao buscar filmes: {e}'})
