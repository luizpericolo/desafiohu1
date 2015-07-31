# coding: utf-8

from django.db import models
from busca.models import BaseModel


class CidadeManager(models.Manager):
	def todos_hoteis_cidade(self, cidade):
		return cidade.hotel_set.all()


class Cidade(BaseModel):
	nome = models.CharField(max_length=255, verbose_name=u"Nome")

	class Meta:
		app_label =	'busca'

	objects = CidadeManager()

	def unicode(self):
		return u"[Id]{} [Nome]{}".format(self.id, self.nome)

	@classmethod
	def search(cls, arg):
		cidades = cls.objects.filter(nome__icontains=arg)
		# typeahead_name é o nome da propriedade que será utlizada para popular o input com o nome da cidade quando ela for selecionada.
		return [{'id': cidade.id, 'typeahead_name': u"{}".format(cidade.nome), 'name': u"{}".format(cidade.nome), 'type': 'cidade'} for cidade in cidades]
