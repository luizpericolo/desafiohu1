# coding: utf-8

import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404

from busca.models import Hotel, Cidade, Disponibilidade

from busca.forms import BuscaHotelForm

def index(request):
	return render(request, 'index.html', {})

def busca_disponibilidade(request):
	u""" View que lista os hotéis que possuem disponibilidade independente do tipo de busca (Hotel ou Cidade, com ou sem período definido). """

	params = request.POST

	# Recuperando os parâmetros enviados pelo form de busca.
	busca = params.get('busca', None)
	id_busca = int(params.get('cidade_hotel_id', 0))
	tipo_busca = params.get('busca_type', None)
	chegada = params.get('entrada', None)
	saida = params.get('saida', None)
	periodo_indefinido = 'periodo_indefinido' in params

	dados = {}

	if tipo_busca == 'cidade':
		# Se buscamos por cidade, queremos saber de todos os hotéis que existem nela.
		try:
			cidade = get_object_or_404(Cidade, id=id_busca)
		except Http404:
			return JsonResponse({'success': False, 'message': 'Erro! A cidade não existe!'})

		hoteis = Hotel.objects.por_cidade(cidade=cidade)

	elif tipo_busca == 'hotel':
		# Se buscamos por hotel, só queremos saber de um em específico.
		try:
			hoteis = [get_object_or_404(Hotel, id=id_busca)]
		except Http404:
			return JsonResponse({'success': False, 'message': 'Erro! O hotel não existe!'})
	else:
		raise ValueError(u"Tipo inválido de busca: {}!".format(tipo_busca))

	if periodo_indefinido:
		# Se não definimos o período, listamos todos os hotéis que a cidade possui
		dados['hoteis'] = [h.serializar() for h in hoteis]
		dados['mensagem_busca'] = u"Você buscou por {}".format(busca)
	else:
		dt_chegada = datetime.datetime.strptime(chegada, "%d/%m/%Y")
		dt_saida = datetime.datetime.strptime(saida, "%d/%m/%Y")

		# Caso contrário, pegamos apenas os hotéis que possuem disponibilidade de pelo menos um dia dentro do período
		hoteis_periodo = filter(lambda h: h.tem_disponibilidade_no_periodo(data_chegada=dt_chegada, data_saida=dt_saida), hoteis)

		dados['hoteis'] = [h.serializar() for h in hoteis_periodo]
		dados['mensagem_busca'] = u"Você buscou por {} no período de {} a {}".format(busca, chegada, saida)
		dados['chegada'] = chegada
		dados['saida'] = saida

	return render(request, 'disponibilidade.html', dados)

def detalhes_disponibilidade(request):
	u""" View que lista os dados de disponibilidade específicos de um hotel. """
	params = request.POST

	chegada = params.get('data_chegada', None)
	saida = params.get('data_saida', None)
	hotel_id = int(params.get('hotel_id', 0))

	dados = {}

	try:
		hotel = get_object_or_404(Hotel, id=hotel_id)
	except Http404:
		return JsonResponse({'success': False, 'message': 'Erro! O Hotel não existe!'})

	if chegada and saida:
		dt_chegada = datetime.datetime.strptime(chegada, "%d/%m/%Y")
		dt_saida = datetime.datetime.strptime(saida, "%d/%m/%Y")
	else:
		dt_chegada, dt_saida = None, None

	disponibilidades = Disponibilidade.objects.por_hotel_periodo(hotel=hotel, data_chegada=dt_chegada, data_saida=dt_saida)

	dados['disponibilidades'] = [d.serializar() for d in disponibilidades]
	dados['hotel'] = hotel.serializar()
	dados['chegada'] = chegada
	dados['saida'] = saida

	return render(request, 'detalhes_disponibilidade.html', dados)

def autocomplete_hotel_cidade(request):
	u""" View que retorna os resultados para o typeahead. """
	query = request.GET.get('q', None)

	if query:
		hoteis = Hotel.search(query)
		cidades = Cidade.search(query)

	return JsonResponse(hoteis+cidades, safe=False)
