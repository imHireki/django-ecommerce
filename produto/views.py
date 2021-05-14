from django.shortcuts import render
from django.views.generic import View, ListView
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    context_object_name = 'produtos'
    template_name = 'produto/lista.html'

class Detalhe(View): pass

class AdicionarAoCarrinho(View): pass

class RemoverDoCarrinho(View): pass

class Carrinho(View): pass

class ResumoDaCompra(View): pass
