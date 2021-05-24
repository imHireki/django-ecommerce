from .models import Pedido, ItemPedido
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from utils import utils
import pprint


class SalvarPedido(View):
    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho')
        if not carrinho:
            messages.error(
                self.request,
                'É necessário adicionar produtos para comprar'
            )
            return redirect('produto:lista')

        # checkar estoque
        
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

        return redirect('produto:lista')
