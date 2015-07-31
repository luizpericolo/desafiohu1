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
		client = Client()

		termo = 'itaborai'

		post_params = {
			'busca': termo,
			'busca_type': 'cidade', # O tipo de busca é cidade.
			'cidade_hotel_id': 78, # O id de itaboraí é 78.
			'entrada': '03/05/2015',
			'saida': '05/05/2015',
		}

		response = client.post(reverse('busca-disponibilidade'), post_params)

		self.assertEquals(response.status_code, 200)

		# Existem 12 hotéis com disponibilidade em itaboraí para o período 03/05/2015 - 05/05/2015.
		self.assertEquals(len(response.context['hoteis']), 12)

	def test_busca_disponibilidade_cidade_existe_sem_periodo(self):
		client = Client()

		termo = 'itaborai'

		post_params = {
			'busca': termo,
			'busca_type': 'cidade', # O tipo de busca é cidade.
			'cidade_hotel_id': 78, # O id de itaboraí é 78.
			'periodo_indefinido': True, # Não estamos passando período para a busca.
		}

		response = client.post(reverse('busca-disponibilidade'), post_params)

		self.assertEquals(response.status_code, 200)

		# Existem 15 hotéis com disponibilidade na cidade itaborai.
		self.assertEquals(len(response.context['hoteis']), 15)

	def test_busca_disponibilidade_cidade_nao_existe_com_periodo(self):
		client = Client()

		termo = 'rio das ostras'

		post_params = {
			'busca': termo,
			'busca_type': 'cidade', # O tipo de busca é cidade.
			'cidade_hotel_id': 30, # O id de rio das ostras é 30.
			'entrada': '01/08/2015',
			'saida': '03/08/2015',
		}

		response = client.post(reverse('busca-disponibilidade'), post_params)

		self.assertEquals(response.status_code, 200)

		# Todas as disponibilidades listadas no banco são para o período 01/05/2015 - 30/05/2015.
		self.assertEquals(len(response.context['hoteis']), 0)

	def test_busca_disponibiliade_hotel_existe_sem_periodo(self):
		client = Client()

		termo = 'casa de hilario'

		post_params = {
			'busca': termo,
			'busca_type': 'hotel', # O tipo de busca é cidade.
			'cidade_hotel_id': 78, # O id de itaboraí é 78.
			'periodo_indefinido': True, # Não estamos passando período para a busca.
		}

		response = client.post(reverse('busca-disponibilidade'), post_params)

		self.assertEquals(response.status_code, 200)

		self.assertEquals(len(response.context['hoteis']), 1)

	def test_busca_disponibiliade_hotel_existe_com_periodo(self):
		client = Client()

		termo = 'casa del embajador'

		post_params = {
			'busca': termo,
			'busca_type': 'hotel', # O tipo de busca é hotel.
			'cidade_hotel_id': 316, # O id de casa del embajador é 78.
			'entrada': '01/05/2015',
			'saida': '03/05/2015',
		}

		response = client.post(reverse('busca-disponibilidade'), post_params)

		self.assertEquals(response.status_code, 200)

		self.assertEquals(len(response.context['hoteis']), 1)

	def test_detalhes_disponibilidade_hotel_existe_com_periodo(self):
		client = Client()

		post_params = {
			'hotel_id': 181, # O id de hotel casa lorenzo é 181.
			'data_chegada': '01/05/2015',
			'data_saida': '06/05/2015',
		}

		response = client.post(reverse('detalhes-disponibilidade'), post_params)

		self.assertEquals(response.status_code, 200)

		# Existe disponibilidade de dois dias para o hotel casa lorenzo no período 01/05/2015 - 06/05/2015
		self.assertEquals(len(response.context['disponibilidades']), 2)

	def test_detalhes_disponibilidade_hotel_existe_sem_periodo(self):
		client = Client()

		post_params = {
			'hotel_id': 7, # O id do hotel george sand é 7.
		}

		response = client.post(reverse('detalhes-disponibilidade'), post_params)

		self.assertEquals(response.status_code, 200)

		# Existe disponibilidade de 21 dias para o hotel george sand.
		self.assertEquals(len(response.context['disponibilidades']), 21)

	def test_detalhes_disponibilidade_hotel_nao_existe_com_periodo(self):
		client = Client()

		post_params = {
			'hotel_id': 6, # O id de hotel pousada são silmares é 6.
			'data_chegada': '30/05/2015',
			'data_saida': '31/05/2015',
		}

		response = client.post(reverse('detalhes-disponibilidade'), post_params)

		self.assertEquals(response.status_code, 200)

		# Não existe disponibilidade para o hotel pousada são silmares no período 30/05/2015 - 31/05/2015
		self.assertEquals(len(response.context['disponibilidades']), 0)