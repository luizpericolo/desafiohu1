#coding: utf-8

from django.db import models
from busca.models import BaseModel

class Hotel(BaseModel):
	nome = models.CharField(max_length=255, verbose_name=u"Nome")
	cidade = models.ForeignKey('busca.Cidade', verbose_name=u"Cidade")
	
	class Meta:
		app_label = 'busca'

	def unicode(self):
		return u"[Id]{} [Nome]{} [Cidade]{}".format(self.id, self.nome, self.cidade.nome)

	@classmethod
	def search(cls, arg):
		hoteis = cls.objects.filter(nome__icontains=arg)
		# typeahead_name é o nome da propriedade que será utlizada para popular o input com o nome do hotel quando ele for selecionado, sem incluir o nome da cidade.
		return [{'id': hotel.id, 'typeahead_name': u'{}'.format(hotel.nome), 'name': u'{}, {}'.format(hotel.nome, hotel.cidade.nome), 'type': 'hotel'} for hotel in hoteis]

