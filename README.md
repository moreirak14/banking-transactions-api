# Banking Transactions API
Sistema de Transações Bancárias com Concorrência de Saldo


## Pré-requisitos

- Python 3.12+: `https://www.python.org/downloads/`
- Docker: `https://docs.docker.com/engine/install/ubuntu/`
- Poetry: `https://python-poetry.org/docs/#installation`
- Make: `https://www.gnu.org/software/make/` (Opcional)


## Necessário

- Com o Docker instalado e antes de criar o ambiente virtual, vamos criar uma imagem Docker para o banco de dados:
  - `$ docker run -e POSTGRES_PASSWORD=banking -e POSTGRES_USER=banking -e POSTGRES_DATABASE=banking -p 5432:5432 -d --name banking_db postgres`

- Com o poetry instalado, basta executar os comandos abaixo para criar a virtualenv e instalar as dependências do projeto:
  - `$ make setup` > Cria a virtualenv e ativa
  - `$ make install` > Instala as dependências do projeto
  - `$ make copy-envs` > Cria o arquivo `.secrets.toml` com as variáveis de ambiente
  - `$ make run-docker` > Cria os containers do banco e da aplicação
  - `$ make db-up` > Executa as migrations


## Executando o Projeto

- O arquivo que será executado está localizado:
  - `./main.py`
- Para executar o projeto, execute:
  - `$ make run`
- Ou se preferir, execute com imagem Docker:
  - `$ make run-docker`


## Documentação Swagger UI

- Após executar o projeto, basta acessar a url:
  - `http://0.0.0.0:8080/docs` ou `http://0.0.0.0:8080/redoc`


## Boas práticas (antes de comitar sua branch)

- Use as funcionalidades do "pré commit" que auxiliará com os ajustes de quebra de linhas, aspas e etc:
  - `$ make pre-commit`


## Executando o script que simula transações bancárias

- Para executar o script que simula transações bancárias, execute:
  - `$ make run-script`

Após executar o script, será possivel inicializar a aplicação e verificar as transações realizadas de cada conta diretamente no Swagger UI.


## Outras informações:

- Para mais informações, acesse o arquivo `Makefile` que estará mapeado todos os comandos necessários para executar o projeto.
- Caso queira saber o que tem mapeado no `Makefile`, execute:
  - `$ make help`
