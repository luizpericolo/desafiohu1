# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.conf import settings

from collections import namedtuple

LinhaHotel = namedtuple('LinhaHotel', ['id', 'cidade', 'nome_hotel']) 
LinhaDisponibilidade = namedtuple('LinhaDisponibilidade', ['hotel_id', 'data', 'disponivel'])

def load_hoteis_cidades(apps, schema_editor):

    print u"Criando hotéis e cidades..."

    Hotel = apps.get_model("busca", "Hotel")
    Cidade = apps.get_model("busca", "Cidade")

    with open(settings.HOTEIS_INITIAL, "r") as f_hoteis:
        for hotel_line in f_hoteis:
            linha_hotel = LinhaHotel(*hotel_line.decode('utf-8').rstrip().split(','))
            
            # Criando ou recuperando a Cidade que está listada no hotel.
            cidade, criada = Cidade.objects.get_or_create(nome=linha_hotel.cidade)

            if criada:
                print u"A cidade {} foi criada!".format(cidade.nome)

            # Precisamos passar o id também, já que se não passarmos o sqlite cria um id maior do que todos os
            #	ids de todas as outras tabelas. E isso faz com que os dados fornecidos sejam inconsistentes.
            hotel = Hotel.objects.create(id=linha_hotel.id, cidade=cidade, nome=linha_hotel.nome_hotel)

            print u"O hotel {} foi criado!".format(hotel.nome)

    print u"Todos os hotéis e cidades foram criadas com sucesso!"

def load_disponibilidades(apps, schema_editor):
    import datetime
    import pudb; pu.db

    print u"Criando disponibilidades..."

    Disponibilidade = apps.get_model("busca", "Disponibilidade")
    Hotel = apps.get_model("busca", "Hotel")

    with open(settings.DISPONIBILIDADES_INITIAL, "r") as f_disponibilidades:
        for disponibilidade_line in f_disponibilidades:
            linha_disponibilidade = LinhaDisponibilidade(*disponibilidade_line.rstrip().split(','))

            # Transformando a entrada que está no formato dd/mm/yyyy em um objeto Date.
            data = datetime.datetime.strptime(linha_disponibilidade.data, "%d/%m/%Y").date()
            
            # Transformando 1 para True e 0 para False
            disponivel = True if int(linha_disponibilidade.disponivel) else False

            disponibilidade = Disponibilidade.objects.create(hotel_id=linha_disponibilidade.hotel_id, data=data, disponivel=disponivel)

            print u"A disponibilidade {} foi criada!".format(disponibilidade)

    print u"Todas as disponibilidades foram criadas com sucesso!"

class Migration(migrations.Migration):

    dependencies = [
        ('busca', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_hoteis_cidades),
        migrations.RunPython(load_disponibilidades),
    ]
