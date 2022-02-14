#  **Teste Python - Plataforma SaaS**

# Descrição
Considere um cenário em que você precisa cadastrar sua empresa para uma plataforma SaaS. <br>

Teste realizado na linguagem python, utilizando framework Django.
Para construção da API Rest foi utilizado a biblioteca Django Rest Framework. <br>
Para construção dos workers assíncronos, foi utilizada a biblioteca Celery, juntamente com RabbitMQ como broker. <br>


# Requisitos
- [Docker](https://docs.docker.com/engine/install/ubuntu/) com [docker-compose](https://docs.docker.com/compose/install/)
- [Make GNU](https://www.gnu.org/software/make/) (Opcional)

<br></br>
# Configurações

* Clone ou faça download do repositório.
```
    git clone https://github.com/edson-dias/teste_saas
```

* Entre na pasta teste_saas.
```
    cd teste_saas/
```

### Caso possua a ferramenta Make instalada:
* Para subir e contruir os containers.
```
    make all
```
* Para desmontar os containers.
```
    make down
```

### Para usuários sem a ferramenta make
* Utilize diretamente a ferramenta docker-compose.
```
    docker-compose up -d
```
Rodando os testes
```
    python src/manage.py test
```
___
<br></br>

# Entrypoint e Endpoints da API
Entrypoint da API: **http://127.0.0.1:8000/api**

* Cadastro de novos usuários
```
   Endpoint: /user/
   Método: POST
   Necessário Autenticação: Não
   json: {
       "first_name": str,
       "last_name": str,
       "email": str,
       "password": str
   }
```

* Cadastro de novas empresas
```
    Endpoint: /company/
    Método: POST
    Necessário Autenticação: Não
    json: {
       "corporate_name": str,
       "trade_name": str,
       "cnpj": str,
       "user": int
   }
```

* Login de usuários. Retorna token para utilização nos endpoints com autenticação necessária
```
    Endpoint: /login/
    Método: POST
    Necessário Autenticação: Não
    json: {
       "username": str,
       "password": str,
   }
```

* Cadastro de membros na empresas
```
    Endpoint: /company/members/registry/
    Método: POST
    Necessário Autenticação: Token
    json: {
       "company_id": int,
       "user_id": int,
   }
```

* Listagem de todas empresas do usuário logado
```
    Endpoint: /user/companies/
    Método: GET
    Necessário Autenticação: Token
    json: {
       "id": int,
       "corporate_name": str,
       "trade_name": str,,
       "cnpj": str,
       "user": list
   }
```

* Listagem de membros de uma empresa específica
```
    Endpoint: /company/<int:id>/members/
    Método: GET
    Necessário Autenticação: Token
    json: {
       "id": int,
       "first_name": str,
       "last_name": str,
       "email": str
   }
```

# Observações

* Arquivo .env contem dados sensíveis da API que não devem ficar expostos. <br>
Para utilização em produção devem ser gerados novas senhas e usuários assim como uma nova secret_key.