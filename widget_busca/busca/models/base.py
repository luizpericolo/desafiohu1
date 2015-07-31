# coding: utf-8

from django.db import models

class BaseModel(models.Model):

	def serializar(self):
		u"""
			Função que serializa todos os models que herdam de BaseModel.
		 """
		dados = {}

		for field in self._meta.fields:
			if isinstance(field, models.DateField):
				dados[field.name] = getattr(self, field.name).strftime("%d/%m/%Y")
			elif hasattr(getattr(self, field.name, None), 'serializar'):
				dados[field.name] = getattr(self, field.name).serializar()
			else:
				dados[field.name] = getattr(self, field.name, None)

		return dados
