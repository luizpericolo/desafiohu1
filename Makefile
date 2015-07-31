install:
	@python widget_busca/manage.py syncdb
	@python widget_busca/manage.py loaddata widget_busca/fixtures/fixture_banco.json

test:
	@python widget_busca/manage.py test busca
