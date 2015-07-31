# coding: utf-8

from django.db import models
from busca.models import BaseModel

class DisponibilidadeManager(models.Manager):
	def por_hotel_periodo(self, hotel, entrada, saida):
		return self.filter(hotel=hotel, data__gte=entrada, data__lte=saida, disponivel=True)

class Disponibilidade(BaseModel):
	hotel = models.ForeignKey('busca.Hotel', verbose_name=u"Hotel")
	data = models.DateField(verbose_name=u"Data")
	disponivel = models.BooleanField(default=True, verbose_name=u"Disponível")

	class Meta:
		app_label = 'busca'

	def unicode(self):
		return u"[Id]{} [Hotel]{} [Data]{} [Disponível]{}".format(self.id, self.hotel.nome, self.data.strftime("%d/%m/%Y"), "Sim" if self.disponivel else "Não")

	objects = DisponibilidadeManager()
