# RainCife RESTful API

*Monitoramento de chuvas e alagamentos na palma da sua mão.* Este repositório
contém somente a API do RainCife, para acessar o repositório da aplicação
em si, clique [aqui](https://github.com/MCRSoftwares/RainCife-API).

## Vagrant
Se não for utilizar o Vagrant, continue [aqui](#pré-requisitos).
Caso esteja utilizando o [Vagrant](https://www.vagrantup.com/), basta executar os comandos abaixo (levará aproximadamente 10-20 minutos para configurar a máquina por completo):
```shell
$ git clone https://github.com/MCRSoftwares/RainCife-API.git
$ cd RainCife-API
$ vagrant up
```

Se ocorrer algum erro, execute:
```shell
$ vagrant provision
```

Caso os erros persistam, baixe esta [máquina virtual (680.20 MB)](https://www.dropbox.com/s/g77vo1x4xruacns/raincife.box?dl=0) e siga para o [próximo passo](#vagrant---instalando-uma-máquina-existente).

Para **acessar** a máquina virtual, execute:
```shell
$ vagrant ssh
```

Para **sair** da máquina virtual, basta executar:
```shell
$ logout
```

Para **desligar** a máquina virtual, execute:
```shell
$ vagrant halt
```

Para **destruir** a máquina virtual, execute:
```shell
$ vagrant destroy
```

Dentro da máquina virtual, execute os seguintes comandos para configurar o servidor do redis e o scrapy (pressione ```ENTER``` sempre que algo for pedido):
```shell
$ cd raincife/
$ make redis.install
& make scrapy.install
```

Caso for usar o PostgreSQL, crie um banco e uma senha para o usuário 'postgres' (essas configurações serão importantes na hora de definir o ```DATABASE_URL```):
```shell
$ createdb raincife
$ sudo su - postgres
$ psql
$ ALTER USER postgres PASSWORD 'senha';
$ \q
$ logout
```

Agora, basta criar uma virtualenv:
```shell
$ mkvirtualenv raincife
```

Tendo o Vagrant configurado e rodando corretamente, pule os próximos passos até chegar em [Configurando o sistema](#configurando).

## Vagrant - Instalando uma máquina existente

Após baixar o arquivo ```raicife.box```, cole-o na pasta do projeto, no mesmo nível do arquivo ```Vagrantfile``` e execute o comando abaixo:
```shell
$ vagrant box add raincife raincife.box
```

Após a execução do comando, tenha certeza de que a máquina virtual anterior (caso tenha tentado criar uma) não exista mais, depois apague o arquivo ```Vagrantfile```:
```shell
$ vagrant destroy
$ rm Vagrantfile
```

Agora, baixe ou copie este [Vagrantfile](https://gist.github.com/victorfsf/f6d802b3b94de8f0a168) e cole onde o antigo ```Vagrantfile``` estava. Dentro da mesma pasta, execute:
```shell
$ vagrant up
$ vagrant ssh
```

Outros comandos do vagrant podem ser encontrado [acima](#vagrant).
Tendo o Vagrant configurado e rodando corretamente, pule os próximos passos até chegar em [Configurando o sistema](#configurando).

## Pré-Requisitos

Para instalar e executar o sistema, deve-se utilizar uma máquina
**Ubuntu** (não testado no Windows) com as seguintes configurações:

|Package                                         |Comando                                 |
|------------------------------------------------|----------------------------------------|
|Git (obviamente)                                |```sudo apt-get install git```          |
|Python 2.7.8 ou Superior (não utilizar Python 3)|Já vem instalado com o Ubuntu           |
|Python-pip                                      |```sudo apt-get install python-pip```   |
|Virtualenv                                      |```sudo pip install virtualenv```       |
|Virtualenv Wrapper                              |```sudo pip install virtualenvwrapper```|
|Configurar e criar uma Virtualenv               | Siga os passos nesse [link](http://roundhere.net/journal/virtualenv-ubuntu-12-10/).                            |
|Iniciar a Virtualenv antes de tudo              |```workon nome_da_venv```               |

Após instalar o que se pede acima, *instale as dependências abaixo:*

### Scrapy

Deve-se instalar as seguintes dependências:
```shell
$ sudo apt-get update
$ sudo apt-get install python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libpq-dev
```
Após aplicar as dependências, instale o Scrapy no Ubuntu:
```shell
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7
$ echo 'deb http://archive.scrapy.org/ubuntu scrapy main' | sudo tee /etc/apt/sources.list.d/scrapy.list
$ sudo apt-get update
$ sudo apt-get install scrapy
$ sudo pip install scrapy
```

### Redis

Baixe e instale o Redis:
```shell
$ wget http://download.redis.io/releases/redis-3.0.4.tar.gz
$ tar xzf redis-3.0.4.tar.gz
$ cd redis-3.0.4
$ make
$ sudo make install
$ cd utils
$ sudo ./install_server.sh
```

### PostgreSQL

Este passo é opcional, mas caso não o siga, recomenda-se que remova a última linha do arquivo ```requirements.txt```, referente à dependencia do ```psycopg2```.

Instale os pacotes do Postgres:
```shell
$ sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-9.4
```

Instale o Psycopg2 para o Python:
```shell
$ sudo apt-get install python-psycopg2
```

Crie uma senha para o usuário 'postgres':
```shell
$ sudo su - postgres
$ psql
$ ALTER USER postgres PASSWORD 'senha';
$ \q
$ logout
```

Crie um banco de dados para a aplicação:
```shell
$ createdb nome_do_banco
```

## Configurando o sistema

Com os pré-requisitos instalados, sua máquina está quase pronta para executar
 o sistema. Mas antes, deve-se baixar a versão mais recente e configurá-la. Siga as instruções abaixo:

### Clonando o Repositório
 ```shell
$ git clone https://github.com/MCRSoftwares/RainCife-API.git
 ```

### Configurando

Uma vez clonado, entre na pasta do repositório (considerando que a **virtualenv** já está ativada):
```shell
$ cd RainCife-API/ (ou 'cd raincife/', se estiver usando o Vagrant)
```

Crie e Configure o arquivo ```settings.ini```. Baseie-se no arquivo
```example.settings.ini``` (mas não o apague). Não é necessário usar todas
as variáveis presentes, somente aquelas cujos valores tenham alguma
importância no momento. Segue abaixo um exemplo do arquivo preenchido.

*O valor da* ```SECRET_KEY``` *foi fornecido à equipe de desenvolvimento.*
```ini
[settings]

# DJANGO SETTINGS

SECRET_KEY=abcdefghijklmnopqrstuvwxyz
DEBUG=True
DATABASE_URL=postgres://usuario:senha@localhost:5432/raincife

# SCRAPY SETTINGS

DJANGO_SETTINGS_MODULE=settings

# CELERY SETTINGS

BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379


```


Agora, basta executar o seguinte comando para instalar os requisitos, configurar
o banco e criar um superuser:
```shell
$ make init
```
Será pedida uma senha para o superuser. Coloque a senha que desejar.

## Comandos do Makefile

Segue abaixo uma lista de comandos para facilitar o desenvolvimento.

### Executar configurações iniciais

```shell
$ make init
```

### Iniciar o servidor do Django

```shell
$ make serve
```

### Instalar os requisitos

```shell
$ make requirements
```

### Sincronizar o banco

```shell
$ make sync
```

### Criar e executar as migrações
Respectivamente:

```shell
$ make makemig
$ make mig
```

### Abrir o shell do Django
```shell
$ make shell
```

### Coletar os arquivos estáticos

```shell
$ make static
```

### Iniciar uma spider

```shell
$ make crawl spider=nome_da_spider
```

### Iniciar e parar o Redis
Respectivamente:

```shell
$ make redis.start
$ make redis.stop
```

### Iniciar o Celery e o Celery Beat
Respectivamente:

```shell
$ make celery
$ make celery.beat
```
