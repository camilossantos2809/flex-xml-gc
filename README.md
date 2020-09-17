# flex-xml-gc

Emissão de guia cega para conferência de recebimento de mercadorias com base nos dados do xml gravado no banco de dados do erp Flex.

Para criação do ambiente virtual utilizar o virtualenv:

    pip install virtualenv
    virtualenv venv

Acessar o ambiente virtual.

**Linux:** `source venv/bin/activate`

**Windows:** `venv\Scripts\activate.bat`

Realizar a instalação das dependências: `pip install -r requirements.txt`

Criar o schema do arquivo de configuração:

    flask db migrate
    flask db upgrade

Executar o webserver utilizado em desenvolvimento para testar a instalação

    flask run
 Não retornando nenhum erro no comando acima a aplicação poderá ser acessada no navegador no endereço http://localhost:5000


**WEBSERVER PRODUÇÃO**

**GNU/Linux**
No caso do GNU/Linux poderá ser utilizado qualquer webserver compatível com o wsgi como o Nginx ou Apache2.

**Windows**
No Windows é necessário utilizar o Apache Lounge (https://www.apachelounge.com/) e instalar o mod_wsgi (`pip install mod_wsgi`).
Para instalação do mod_wsgi no Windows é necessária a instalação no Visual Studio C++ Build Tools (https://www.visualstudio.com/downloads) incluindo Windows SDK 8 e 10.

Para identificar os valores a ser informados na configuração do apache, executar: `mod_wsgi-express module-config`.

No projeto em `docs/examples` existem alguns exemplos de configuração para o Apache.
