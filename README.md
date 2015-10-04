# RainCife RESTful API

*Monitoramento de chuvas e alagamentos na palma da sua mão.* Este repositório
contém somente a API do RainCife, para acessar o repositório da aplicação
em si, clique [aqui](https://github.com/MCRSoftwares/RainCife-API)

## Pré-Requisitos

Para instalar e rodar o sistema, deve-se utilizar uma máquina
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

ESte passo é opcional, mas caso não o siga, recomenda-se que remova a última linha do arquivo ```requirements.txt```, referente à dependencia do ```psycopg2```.

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
$ ALTER USER postgres PASSWORD 'newpassword';
$ \q
$ logout
```

Crie um banco de dados para a aplicação:
```shell
$ createdb nome_do_banco
```

## Configurando o sistema

Com os pré-requisitos instalados, sua máquina está quase pronta para rodar
 o sistema. Mas antes, deve-se baixar a versão mais recente e configurá-la. Siga as instruções abaixo:

 ### Clonando o Repositório
 ```shell
$ git clone https://github.com/MCRSoftwares/RainCife-API.git
 ```

 ### Configurando

Uma vez clonado, entre na pasta do repositório:
```shell
$ cd RainCife-API/
```

Crie e Configure o arquivo ```settings.ini```. Baseie-se no arquivo ```example.settings.ini``` (mas não o apague). Segue abaixo um exemplo do arquivo preenchido.
*O valor da* ```SECRET_KEY``` *foi fornecido à equipe de desenvolvimento.*
```ini
[settings]

# DJANGO SETTINGS

SECRET_KEY=abcdefghijklmnopqrstuvwxyz
DEBUG=True
DATABASE_URL=postgres://usuario:senha@localhost:5432/raincife
# ADMIN_URL=admin

# SCRAPY SETTINGS

DJANGO_SETTINGS_MODULE=settings

# CELERY SETTINGS

BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379


```


Agora, basta rodar o seguinte comando para instalar os requisitos, configurar
o banco e criar um superuser:
```shell
$ make init
```
Será pedida uma senha para o superuser. Coloque a senha que desejar.
