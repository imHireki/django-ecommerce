from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    # many Pedido to one User
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    qtd_total = models.PositiveIntegerField()
    total = models.FloatField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado')
        )
    )

    def __str__(self):
        return str(self.id)

    
class ItemPedido(models.Model):
    # Many ItemPedido to one Pedido
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField(default=1)
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
