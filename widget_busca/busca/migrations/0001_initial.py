# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('basemodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='busca.BaseModel')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
            ],
            bases=('busca.basemodel',),
        ),
        migrations.CreateModel(
            name='Disponibilidade',
            fields=[
                ('basemodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='busca.BaseModel')),
                ('data', models.DateField(verbose_name='Data')),
                ('disponivel', models.BooleanField(default=True, verbose_name='Dispon\xedvel')),
            ],
            bases=('busca.basemodel',),
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('basemodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='busca.BaseModel')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', to='busca.Cidade')),
            ],
            bases=('busca.basemodel',),
        ),
        migrations.AddField(
            model_name='disponibilidade',
            name='hotel',
            field=models.ForeignKey(verbose_name='Hotel', to='busca.Hotel'),
        ),
    ]
