from django import template
from utils import utils


register = template.Library()

@register.filter
def formata_preco(val):
    return utils.formata_preco(val)
