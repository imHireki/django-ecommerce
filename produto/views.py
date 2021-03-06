from pedido.views import Lista
from django import http
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from . import models
from django.contrib import messages
from perfil.models import Perfil
from django.db.models import Q
import requests


class ListaProdutos(ListView):
    model = models.Produto
    context_object_name = 'produtos'
    template_name = 'produto/lista.html'
    paginate_by = 1
    ordering = ['-id']


class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session.get('termo')

        if not termo:
            return super().get_queryset(*args, **kwargs)

        self.request.session['termo'] = termo
        
        q = models.Produto.objects.filter(
            Q(nome__contains=termo) |
            Q(descricao_curta__contains=termo) |
            Q(descricao_longa__contains=termo)
        )
        

        self.request.session['termo'] = termo
        self.request.session.save()

        return q


class Detalhe(DetailView):
    model = models.Produto
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
    template_name = 'produto/detalhe.html'
    

class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        vid = self.request.GET.get('vid')
        
        vid_db = models.Variacao.objects.filter(
            id=vid
        ).first()

        if not vid_db: 
            messages.error(
                self.request,
                'Produto inválido'
            )
            return redirect(http_referer)

        carrinho = self.request.session.get('carrinho')
        if not carrinho:
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        carrinho = self.request.session['carrinho']
        estoque = vid_db.estoque
        produto_id = vid_db.produto.id
        produto_nome = vid_db.produto.nome
        variacao_nome = vid_db.nome or vid_db.produto.nome
        preco_unitario = vid_db.preco
        preco_unitario_promocional = vid_db.preco_promocional
        slug = vid_db.produto.slug
        imagem = vid_db.produto.imagem

        if imagem:
            imagem = imagem.name    

        if vid in carrinho.keys():
            quantidade = carrinho[vid]['quantidade'] + 1
            if estoque < quantidade:
                messages.warning(
                    self.request,
                    'estoque insuficiente!'
                )
                return redirect(http_referer)

            new_quant = carrinho[vid]['preco_unitario'] * quantidade
            new_quant_promo = carrinho[vid]['preco_unitario_promocional'] * quantidade

            carrinho[vid]['preco_quantitativo'] = new_quant
            carrinho[vid]['preco_quantitativo_promocional'] = new_quant_promo
            carrinho[vid]['quantidade'] = quantidade

            
        else:
            carrinho[vid] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': vid,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        
        messages.success(
            self.request,
            'Produto adicionado com sucesso!'
        )

        self.request.session.save()
            
        return redirect(http_referer)



class Carrinho(View):
    template_name = 'produto/carrinho.html'

    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho', {})
        
        # TODO: rest
        # a = requests.get(
        #     'http://127.0.0.1:8000/api/users/',
        # ).json()
        # print(a)
        # import requests
        
        contexto = {
            'carrinho': carrinho
        }
        
        return render(
            self.request, self.template_name, contexto
        )


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('produto:carrinho')
        )
        vid = self.request.GET.get('vid')
        carrinho = self.request.session.get('carrinho')

        if not carrinho or not vid in carrinho:
            return redirect(http_referer)
        
        del self.request.session['carrinho'][vid]
        self.request.session.save()

        return redirect(http_referer)


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Cadastro ou Login necessários para comprar'
            )
            return redirect('perfil:criar')
        
        perfil = Perfil.objects.filter(
            usuario=self.request.user
        ).exists()
        
        if not perfil:
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            return redirect('produto:lista')
        
        template_name = 'produto/resumo.html'
        
        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session.get('carrinho')
        }
        
        return render(self.request, template_name, contexto)
