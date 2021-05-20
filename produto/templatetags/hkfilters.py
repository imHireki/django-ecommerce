from utils import utils
from django import template


register = template.Library()

@register.filter
def formata_preco(val):
    return utils.formata_preco(val)

@register.filter
def get_total(carrinho) -> str:
    return utils.get_total(carrinho)
    