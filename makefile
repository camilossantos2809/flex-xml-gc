# SHELL := '/bin/bash'
export FLASK_APP=app.py
export FLASK_ENV=development

run:
	flask run

# Efetua a criação inicial do banco de dados.
# Executar make upgrade para criar as tabelas conforme última migração
migrate:
	flask db migrate

# Cria o schema contido nos arquivos de migração do alembic
upgrade:
	flask db upgrade

git-log:
	git log --graph --oneline --decorate -n 5

git-log+:
	git log --stat --graph --decorate

# Atualiza os pacotes instalados
pip-upgrade:
	pip install --upgrade $$(pip list --format=freeze | cut -d = -f 1);
	pip freeze > requirements.txt
	sed -i ':a;N;$$!ba;s/pkg-resources==0.0.0\n//g' requirements.txt

# Executa os testes do projeto e exibe saída simplificada no terminal
test:
	python -m unittest discover

# Executa os testes do projeto e exibe informações detalhadas de cada "test case"
test-detailed:
	python -m unittest discover -v

#Deleta arquivos com extensão pyc do módulo tests
delete-pyc:
	find ./tests -name "*.pyc" -delete

# Gera relatório de cobertura de testes em formato HTML
coverage-html:
	coverage run setup.py test
	coverage html
	brave htmlcov/index.html 2> /dev/null

# Gera relatório de cobertura de testes simplificado no terminal
coverage:
	coverage run setup.py test
	coverage report
