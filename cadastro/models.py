from django.db import models

class FilmeSerie(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    descricao = models.TextField()
    capa = models.ImageField(upload_to='filmes_capas/', blank=True, null=True)
    assistido = models.BooleanField(default=False)
    def __str__(self):
        return self.nome
