# coding: utf-8

from django.db import models
from busca.models import BaseModel

class Cidade(BaseModel):
	nome = models.CharField(max_length=255, verbose_name=u"Nome")

	class Meta:
		app_label =	'busca'

	def unicode(self):
		return u"[Id]{} [Nome]{}".format(self.id, self.nome)

	@classmethod
	def search(cls, arg):
		return cls.objects.filter(nome__icontains=arg)

