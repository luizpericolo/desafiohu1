from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

from busca.models import Hotel, Cidade

from busca.forms import BuscaHotelForm

def index(request):
	return render(request, 'index.html', {})

def busca_disponibilidade(request):
	return render(request, 'disponibilidade.html', {})

def autocomplete_hotel_cidade(request):
	query = request.GET.get('q', None)

	if query:
		hoteis = Hotel.search(query)
		cidades = Cidade.search(query)

	return JsonResponse(hoteis+cidades, safe=False)
