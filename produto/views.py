from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    context_object_name = 'produtos'
    template_name = 'produto/lista.html'

class Detalhe(DetailView):
    model = models.Produto
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
    template_name = 'produto/detalhe.html'
    

class AdicionarAoCarrinho(View): pass

class RemoverDoCarrinho(View): pass

class Carrinho(View): pass

class ResumoDaCompra(View): pass
