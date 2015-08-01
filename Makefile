install-dependencies: configure-virtualenv
	@echo "Instalando as dependências do pip..."
	@venv/bin/pip install -r requirements.txt
	@echo "Por favor execute o comando 'source venv/bin/activate' para ativar o virtualenv e depois continue a instalação com 'make deploy'"

install: install-dependencies

install-virtualenv:
	@echo "Instalando virtualenv..."
	@sudo easy_install virtualenv

configure-virtualenv: install-virtualenv
	@echo "Configurando virtualenvwrapper..."
	@virtualenv venv

run:
	@echo "Executando o servidor local..."
	@python widget_busca/manage.py runserver

deploy: sync-db test run

sync-db:
	@echo "Sincronizando o banco..."
	@python widget_busca/manage.py syncdb
	@echo "Importando os dados iniciais..."
	@python widget_busca/manage.py loaddata widget_busca/fixtures/fixture_banco.json

test:
	@echo "Rodando testes unitários..."
	@python widget_busca/manage.py test busca
