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

