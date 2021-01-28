from django.views.generic import ListView, DetailView
from drama.models import Genre, Drama


class GenreLV(ListView):
    model = Genre


class GenreDV(DetailView):
    model = Genre


class DramaDV(DetailView):
    model = Drama

