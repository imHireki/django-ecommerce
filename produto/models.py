from django.db import models
from django.conf import settings
from django.contrib import admin
from utils import utils
from PIL import Image
import os


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/', blank=True, null=True
    )
    slug = models.CharField(max_length=512, unique=True, blank=True, null=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        max_length=1,
        default='V',
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples')
        )
    )

    @admin.display(description='Preço')
    def preco_marketing_f(self):
        return utils.formata_preco(self.preco_marketing)

    @admin.display(description='Preço promocional')
    def preco_marketing_promocional_f(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    
    def __str__(self):
        return self.nome

    @staticmethod
    def resize_image(img, new_width):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        image = Image.open(img_full_path)
        original_width, original_height = image.size

        if original_width <= new_width:
            image.save(img_full_path)

        new_height = round((new_width * original_height) / original_width)
        
        resize = image.resize((new_width, new_height), Image.LANCZOS)

        resize.save(img_full_path)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)    
        max_width = 800

        if self.imagem:
            self.resize_image(self.imagem, max_width)

        
class Variacao(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
        