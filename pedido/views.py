from django.http import HttpResponse
from django.views.generic import View
from produto.models import Variacao
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from utils import utils
from .models import ItemPedido, Pedido


class Pagar(View):
    pass


class SalvarPedido(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            pass
            
        if not self.request.session.get('carrinho'):
            pass

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]

        bd_variacoes = list(
            Variacao.objects.select_related('produto').filter(
                id__in=carrinho_variacao_ids
            )
        )

        for variacao in bd_variacoes:
            vid = str(variacao.id)
            estoque = variacao.estoque

            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']
        
            warning_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque

                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo

                warning_msg_estoque = 'warning sla'

            if warning_msg_estoque:
                messages.warning(
                    self.request,
                    warning_msg_estoque
                )
                self.request.session.save()
                return redirect('produto:carrinho')

            qtd_total_carrinho = utils.cart_total_qtd(carrinho)
            valor_total_carrinho = utils.cart_totals(carrinho)

            pedido = Pedido(
                usuario=self.request.user,
                total=valor_total_carrinho,
                qtd_total=qtd_total_carrinho,
                status='C'
            )
            pedido.save()

            ItemPedido.objects.bulk_create(
                [
                    ItemPedido(
                        pedido=pedido,
                        produto=v['produto_nome'],
                        produto_id=v['produto_id'],
                        variacao=v['variacao_nome'],
                        variacao_id=v['variacao_id'],
                        preco=v['preco_quantitativo'],
                        preco=v['preco_quantitativo_promocional'],
                        quantidade=v['quantidade'],
                        imagem=v['imagem'],

                    ) for v in carrinho.values()
                ]
            )
            
            del self.request.session['carrinho']

            return redirect(
                reverse(
                    'pedido:pagar',
                    kwargs={'pk': pedido.pk}
                )
            )



class Detalhe(View):
    pass
