from django import forms

class BuscaHotelForm(forms.Form):
	hotel_cidade = forms.CharField(label="hotel_cidade", max_length=100)