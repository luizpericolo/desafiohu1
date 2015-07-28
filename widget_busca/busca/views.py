from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.

from busca.forms import BuscaHotelForm

def index(request):
	return render(request, 'index.html', {})

def busca_disponibilidade(request):
	return render(request, 'disponibilidade.html', {})

def autocomplete_hotel_cidade(request):
	response = JsonResponse([{'id': 10, "name": 'Test'}], safe=False)

	return response
