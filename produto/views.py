from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, TemplateView


class ListaProdutos(TemplateView):
    template_name = 'produto/lista.html'
    

class Detalhe(View): pass

class AdicionarAoCarrinho(View): pass

class RemoverDoCarrinho(View): pass

class Carrinho(View): pass

class ResumoDaCompra(View): pass
