from django.http import HttpResponse
from django.views.generic import View, DetailView, ListView
from produto.models import Variacao
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from utils import utils
from .models import ItemPedido, Pedido


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs

class Lista(DispatchLoginRequiredMixin, ListView):
    template_name = 'pedido/lista.html'
    model = Pedido
    context_object_name = 'pedidos'
    paginate_by = 10
    orderig = ['-id']


class Detalhe(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/detalhe.html'
    model = Pedido
    context_object_name = 'pedido'
    pk_url_kwarg = 'pk'


class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class SalvarPedido(View):
    # Gets here when click on "realizar pedido e pagar" in resumodacompra.html
    def get(self, *args, **kwargs):

        # it's not logged in
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login'
            )
            return redirect('perfil:criar')

        # it has no cart
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio'
            )
            return redirect('produto:lista')

        # Gets variacao ids ['5', '2'] that are keys in carrinho
        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]
        
        # Variacao in db [<Variacao: variacao aaaaaa>, <Variacao: variação b>]
        bd_variacoes = list(
            # 3 queries produto_variacao, produto_produto, produto_produto
            # Variacao.objects.filter(id__in=carrinho_variacao_ids)

            # 1 query produto_variacao (debug_toolbar)
            Variacao.objects.select_related('produto').filter(
                id__in=carrinho_variacao_ids
            )
        )

        for variacao in bd_variacoes:
            # variacao {'id': 1, 'produto_id': 1, 'nome': 'variacao aaaaaa',
            #  'preco': 123123.0, 'preco_promocional': 123.0, 'estoque': 1}
        
            vid = str(variacao.id) # int
            estoque = variacao.estoque

            # carrinho values
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            # warning not active
            warning_msg_estoque = ''

            # admin had decreased the stock and product was already on cart
            if estoque < qtd_carrinho:
                # decreases quantidade on cart of a VID, 4 the max on estoque
                carrinho[vid]['quantidade'] = estoque

                # adjusts all already sum prices, 4 the new quantidade
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unt_promo

                # TRIGGER UP the warning
                warning_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por Favor, '\
                    'verifique quais produtos foram afetados, a seguir:'

            # if estoque < qtd_carrinho, it falls here
            if warning_msg_estoque:
                messages.warning(
                    self.request,
                    warning_msg_estoque
                )
                self.request.session.save()
                return redirect('produto:carrinho')
        
        # passes through utils and get sum of it
        qtd_total_carrinho = utils.cart_total_qtd(carrinho) # variation_id 
        valor_total_carrinho = utils.cart_totals(carrinho) # all prices

        # register on db pedido_pedido:
        # id| total | status | usuario_id | qtd_total
        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )
        pedido.save()

        # register on db all those values in  pedido_itempedido
        # maybe because of pedido=pedido right below
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                
                # carrinho.values() get those v[''] values
                ) for v in carrinho.values() 
            ]
        )

        # del the no needed cart
        del self.request.session['carrinho']

        # redirects to pedido/pagar/pk
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={'pk': pedido.pk}
            )
        )
