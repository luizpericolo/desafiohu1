install-dependencies:
	@echo "Instalando as dependências..."
	@apt-get install python-virtualenv
	@virtualenv venv && source venv/bin/activate
	@echo "Instalando as dependências do pip..."
	@pip install -r requirements.txt

install: install-dependencies deploy test run

run:
	@echo "Executando o servidor local..."
	@python widget_busca/manage.py runserver

deploy:
	@echo "Sincronizando o banco..."
	@python widget_busca/manage.py syncdb
	@echo "Importando os dados iniciais..."
	@python widget_busca/manage.py loaddata widget_busca/fixtures/fixture_banco.json

test:
	@echo "Rodando testes unitários..."
	@python widget_busca/manage.py test busca
