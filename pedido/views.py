from .models import Pedido, ItemPedido
from produto.models import Variacao
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from utils import utils


class Lista(ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'


class Detalhe(DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'


class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('hm')


class SalvarPedido(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                'É necessário estar logado para comprar'
            )
            return redirect('produto:lista')
        
        carrinho = self.request.session.get('carrinho')
        if not carrinho:
            messages.error(
                self.request,
                'É necessário adicionar produtos para comprar'
            )
            return redirect('produto:lista')

        variations = [v for v in carrinho]
        bd_variations = Variacao.objects.filter(
            id__in=variations
        )

        for bd_v in bd_variations:

            vid = str(bd_v.id)
            estoque = bd_v.estoque
            quantidade = carrinho[vid]['quantidade']

            if estoque < quantidade:
                carrinho[vid]['quantidade'] = estoque
                
                unitario = carrinho[vid]['preco_unitario']
                uni_promo = carrinho[vid]['preco_unitario_promocional']

                carrinho[vid]['preco_quantitativo'] = estoque * unitario
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * uni_promo

                messages.warning(
                    self.request,
                    'Estoque insuficiente para alguns produtos do carrinho '\
                    'Quantidade reduzida, verifique e continue a compra.'
                )
                self.request.session.save()
                return redirect(
                    reverse()
                )
        
        qtd_total = utils.get_qtd_total(carrinho)
        preco_total = utils.get_total(carrinho)
        
        pedido = Pedido(
            total=preco_total,
            status='C',
            usuario_id=self.request.user.pk,
            qtd_total=qtd_total,
        )
        pedido.save()

        pedido_id = pedido.id
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido_id=pedido_id,
                    produto_id=item['produto_id'],
                    produto=item['produto_nome'],
                    variacao_id=item['variacao_id'],
                    variacao=item['variacao_nome'],
                    preco=item['preco_quantitativo'],
                    preco_promocional=item['preco_quantitativo_promocional'],
                    quantidade=item['quantidade'],
                    imagem=item['imagem'],
                ) for item in carrinho.values()
            ]
        )

        del self.request.session['carrinho']
        self.request.session.save()


        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={'pk':pedido_id}
            )
        )
