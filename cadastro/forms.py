from django import forms
from .models import FilmeSerie

class FilmeSerieForm(forms.ModelForm):
    class Meta:
        model = FilmeSerie
        fields = ['nome', 'categoria', 'descricao', 'capa']
