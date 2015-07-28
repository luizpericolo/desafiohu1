from django.db import models

class BaseModel(models.Model):

	def serializar(self):
		dados = {}

		for field in self._meta.fields:
			if hasattr(self, 'serializar'):
				dados[field.name] = getattr(self, 'serializar')
			else:
				dados[field.name] = getattr(self, field.name, None)

		return dados
