# coding: utf-8

from django.test import TestCase, Client

from busca.models import Hotel, Cidade, Disponibilidade
from django.core.urlresolvers import reverse

from busca.views import busca_disponibilidade, detalhes_disponibilidade, autocomplete_hotel_cidade

class BuscaTestCase(TestCase):
	fixtures = ['fixture_banco.json']

	def test_autocomplete_hotel_existente_nome_completo(self):
		client = Client()

		termo = 'hotel george sand'
		response = client.get(reverse('autocomplete-hotel-cidade'), {'q': termo})

		self.assertEquals(response.status_code, 200)

		response_data = eval(response.content)

		# Existe apenas um hotel com esse nome
		self.assertEquals(len(response_data), 1)

		# O nome completo do hotel é o nome do hotel seguido pelo nome da cidade
		self.assertEquals(response_data[0].get('name').lower(), u'hotel george sand, saquarema')

	def test_autocomplete_hotel_existente_nome_typeahead_tipo(self):
		client = Client()

		termo = 'hotel george sand'
		response = client.get(reverse('autocomplete-hotel-cidade'), {'q': termo})

		self.assertEquals(response.status_code, 200)

		response_data = eval(response.content)

		# O nome que deve aparecer no typehead, após o hotel ser selecionado é apenas o nome do hotel.
		self.assertEquals(response_data[0].get('typeahead_name').lower(), u'hotel george sand')
		# O tipo do registro retornado para o autocomplete deve ser hotel.
		self.assertEquals(response_data[0].get('type').lower(), u'hotel')

	def test_autocomplete_hotel_existente_nome_parcial(self):
		client = Client()

		termo = 'casa'
		response = client.get(reverse('autocomplete-hotel-cidade'), {'q': termo})

		self.assertEquals(response.status_code, 200)

		response_data = eval(response.content)

		# Existem seis hotéis com esse nome
		self.assertEquals(len(response_data), 6)

		#import pudb; pudb.set_trace()
		# Garantindo que todas as respostas contém o termo buscado.
		self.assertTrue(response_data[0].get('name').lower().find(termo) != -1)
		self.assertTrue(response_data[1].get('name').lower().find(termo) != -1)
		self.assertTrue(response_data[2].get('name').lower().find(termo) != -1)
		self.assertTrue(response_data[3].get('name').lower().find(termo) != -1)
		self.assertTrue(response_data[4].get('name').lower().find(termo) != -1)
		self.assertTrue(response_data[5].get('name').lower().find(termo) != -1)
		# O tipo dos registros retornados para o autocomplete deve ser hotel.
		self.assertEquals(response_data[0].get('type').lower(), u'hotel')
		self.assertEquals(response_data[1].get('type').lower(), u'hotel')
		self.assertEquals(response_data[2].get('type').lower(), u'hotel')
		self.assertEquals(response_data[3].get('type').lower(), u'hotel')
		self.assertEquals(response_data[4].get('type').lower(), u'hotel')
		self.assertEquals(response_data[5].get('type').lower(), u'hotel')

	def test_autocomplete_hotel_inexistente(self):
		client = Client()

		response = client.get(reverse('autocomplete-hotel-cidade'), {'q': 'terra do nunca'})

		self.assertEquals(response.status_code, 200)

		response_data = eval(response.content)

		# Não existem hotéis ou cidades com esse nome.
		self.assertEquals(len(response_data), 0)

	def test_autocomplete_cidade_existente_nome_completo(self):
		client = Client()

		response = client.get(reverse('autocomplete-hotel-cidade'), {'q': 'penedo'})

		self.assertEquals(response.status_code, 200)

		response_data = eval(response.content)

		# Só existe uma cidade com esse nome. Não existem hotéis com penedo no nome.
		self.assertEquals(len(response_data), 1)

		self.assertEquals(response_data[0].get('type').lower(), 'cidade')

	def test_autocomplete_cidade_existente_nome_parcial(self):
		client = Client()

		termo = 'camp'

		response = client.get(reverse('autocomplete-hotel-cidade'), {'q': termo})

		self.assertEquals(response.status_code, 200)

		response_data = eval(response.content)

		# Só existem duas cidades com esse nome parcial. Não existem hotéis com penedo no nome.
		self.assertEquals(len(response_data), 2)

		self.assertTrue(response_data[0].get('name').lower().find(termo) != -1)
		self.assertTrue(response_data[0].get('name').lower().find(termo) != -1)

		self.assertEquals(response_data[0].get('type').lower(), 'cidade')
		self.assertEquals(response_data[1].get('type').lower(), 'cidade')

	def test_autocomplete_cidade_inexistente(self):
		client = Client()

		termo = 'paris'

		response = client.get(reverse('autocomplete-hotel-cidade'), {'q': termo})

		self.assertEquals(response.status_code, 200)

		response_data = eval(response.content)

		# Não existe nenhuma cidade com esse nome.
		self.assertEquals(len(response_data), 0)

	def test_busca_disponibilidade_cidade_existe_com_periodo(self):
		pass

	def test_busca_disponibilidade_cidade_existe_sem_periodo(self):
		pass

	def test_busca_disponibilidade_cidade_nao_existe(self):
		pass

	def test_busca_disponibiliade_hotel_existe_com_periodo(self):
		pass

	def test_busca_disponibiliade_hotel_existe_sem_periodo(self):
		pass

	def test_detalhes_disponibilidade_hotel_existe_com_periodo(self):
		pass

	def test_detalhes_disponibilidade_hotel_existe_sem_periodo(self):
		pass

	def test_detalhes_disponibilidade_hotel_nao_existe_com_periodo(self):
		pass

	# test_detalhes_disponibilidade_hotel_nao_existe_sem_periodo não faz sentido. Né?

	# falta algum?
