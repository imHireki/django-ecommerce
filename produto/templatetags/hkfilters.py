from django import template
from utils import utils


register = template.Library()

@register.filter
def formata_preco(val):
    return utils.formata_preco(val)

@register.filter
def cart_totals(cart):
    return utils.cart_totals(cart)

@register.filter
def total_qtd(cart):
    return utils.total_qtd(cart)
