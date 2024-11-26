from django.shortcuts import render, get_object_or_404, redirect
from .models import FilmeSerie
from .forms import FilmeSerieForm
import logging


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