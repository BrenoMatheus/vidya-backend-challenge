# vidya-backend-challenge

## Contexto do Desafio

Este projeto foi desenvolvido como solução para um desafio técnico backend,
com foco em modelagem de arquitetura, integração entre múltiplos bancos de dados
e implementação de busca textual eficiente sobre dados de vendas.

## Descrição da Solução

Esta aplicação é um backend desenvolvido para gerenciamento de vendas com capacidade avançada de busca textual, integrando dois bancos de dados com responsabilidades distintas:

 * PostgreSQL: armazenamento transacional das vendas (dados estruturados).

 * MongoDB: armazenamento e busca de textos livres relacionados às vendas (comentários, descrições, observações), utilizando Full-Text Search.

A solução foi projetada seguindo princípios de Clean Architecture, separação de responsabilidades e baixo acoplamento, permitindo que cada tecnologia seja utilizada onde faz mais sentido.

O principal diferencial da aplicação é a integração entre os bancos, onde:

 * A busca textual ocorre no MongoDB.

 * Os resultados são correlacionados com registros de vendas no PostgreSQL.

 * O cliente recebe uma resposta consolidada e paginada.

## Principais Decisões Arquiteturais

 * Poliglot Persistence: cada banco resolve um problema específico.

 * Search como Orquestrador: o SearchService atua como camada de coordenação entre MongoDB e PostgreSQL.

 * Repositories isolados por banco: não há SQL dentro de serviços de busca textual nem MongoDB dentro do domínio de vendas.

 * Integração em nível de Service, não de Controller.

 * Full-Text Search nativo do MongoDB, com indexação automática via Docker.

## Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI** – framework web
- **SQLAlchemy** – ORM para PostgreSQL
- **PostgreSQL 15** – banco relacional
- **MongoDB 6** – banco NoSQL com Full-Text Search
- **PyMongo** – driver MongoDB
- **Docker & Docker Compose** – ambiente de execução
- **Uvicorn** – servidor ASGI

## Estrutura Geral da Aplicação

A aplicação segue uma **arquitetura em camadas**, inspirada em princípios de
**Clean Architecture** e **DDD leve**, priorizando:

- manutenibilidade
- testabilidade
- isolamento de regras de negócio
- facilidade de evolução

``` bash 
app/
├── core/           # Configuração e infraestrutura
├── models/         # Modelos de dados (SQL e Mongo)
├── repositories/   # Acesso a dados (Postgres e Mongo)
├── services/       # Regras de negócio e orquestração
├── routes/         # Camada HTTP (FastAPI)
├── schemas/        # Contratos de entrada e saída (DTOs)
├── main.py         # Bootstrap da aplicação

```
 
### Camadas e Responsabilidades

#### `core/` & `infra/`
Centraliza a infraestrutura. Gerencia o ciclo de vida das conexões (**PostgreSQL** via SQLAlchemy e **MongoDB** via PyMongo) utilizando o padrão **Dependency Injection** do FastAPI para prover sessões de banco (`get_db`, `get_mongo_db`) de forma segura e performática.

#### `models/` & `schemas/` (Contratos de Dados)
* **Models:** Representam o estado persistido. Separamos dados transacionais e relacionais (**Postgres**) de dados não-estruturados/textuais (**Mongo**).
* **Schemas (DTOs):** Garantem a integridade do contrato da API usando **Pydantic**. O desacoplamento entre Model e Schema permite que o banco evolua sem impactar os clientes da API.

#### `repositories/` (Persistência)
Implementa o **Repository Pattern**. Esta camada isola a lógica de acesso a dados, permitindo que o restante da aplicação desconheça a origem do dado (SQL ou NoSQL).
* **Full-Text Search:** O `text_repository.py` gerencia índices complexos e buscas por *score* no MongoDB, abstraindo a complexidade de queries textuais.

#### `services/` (Lógica de Domínio)
Onde reside a inteligência do negócio e a orquestração entre bancos.
* **Agregação de Dados:** O `search_service.py` realiza a integração *cross-database*. Ele consulta o MongoDB para busca textual, recupera IDs de referência e hidrata os objetos através do PostgreSQL.
* **Regra de Negócio:** Centraliza cálculos, métricas e fluxos complexos, mantendo as rotas "magras" (**Skinny Controllers**).

#### `routes/` (Interface de Entrega)
Camada puramente de transporte (HTTP). Responsável por:
* Validação de entrada via **Schemas**.
* Invocação do **Service** apropriado.
* Retorno de **Status Codes HTTP** semânticos e documentação via Swagger/OpenAPI.

---

### Infraestrutura e Deployment

O projeto é totalmente conteinerizado, garantindo paridade entre ambientes de desenvolvimento e produção.

* **Docker Compose:** Orquestra o ecossistema completo (API + Postgres + Mongo).
* **Database Provisioning:** O ambiente inclui scripts de inicialização para o MongoDB que automatizam a criação de **Text Indexes**, essenciais para a performance da busca textual desde o primeiro `docker-compose up`.

> **Decisão Arquitetural:** A escolha do **MongoDB** para descrições e textos livres deve-se à flexibilidade de schema e superioridade em buscas textuais (*Full-text search*), enquanto o **PostgreSQL** garante a integridade referencial e consistência dos dados transacionais de vendas.

## Fluxo da Busca Integrada

1. O cliente envia um texto para /search.

2. O MongoDB executa Full-Text Search sobre sale_texts.

3. Os sale_id encontrados são extraídos.

4. O PostgreSQL retorna os registros de vendas correspondentes.

5. A resposta final contém:

    * Dados da venda

    * Tipo do texto (comment, description, observation)

    * Score da busca (quando aplicável)

    * Metadados de paginação

## Instruções para Executar o Projeto
1. Pré-requisitos

    * Docker
    * Docker Compose

2. Clonar o repositório

```bash
git clone https://github.com/BrenoMatheus/vidya-backend-challenge.git
cd vidya-backend-challenge
```

3. Subir a aplicação
```bash
docker-compose up --build
```

Isso irá subir:

    * API FastAPI (http://localhost:8000)
    * PostgreSQL (5432)
    * MongoDB (27017)

4. Comando para executar o seed

Com os containers já em execução, rode:

```bash
docker exec -it sales_api python -m scripts.seed_data
```

5. Acessar a documentação da API

```bash
http://localhost:8000/docs
```

## Exemplo de Busca Integrada
 - Request

```bash
POST /search
Content-Type: application/json
```

```bash
{
  "text": "Cliente"
}
```

Response (exemplo)
```bash
{
  "items": [
    {
      "sale": {
        "id": 1,
        "product_name": "Notebook Pro",
        "category": "Eletrônicos",
        "quantity": 5,
        "unit_price": 3500.0,
        "sale_date": "2026-01-15"
      },
      "text": "Cliente muito satisfeito, elogiou a velocidade e o acabamento.",
      "type": "comment",
      "score": 1.2
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "pages": 1
  }
}
```

## Boas Práticas e Padrões Utilizados

- Clean Architecture
- Repository Pattern
- Service Layer
- Dependency Injection (FastAPI)
- DTOs com Pydantic
- Skinny Controllers
- Poliglot Persistence

## Evoluções Futuras

 * Cache de resultados de busca (Redis)
 * Ranking híbrido (text score + métricas de venda)
 * Autenticação e autorização
 * Indexação assíncrona via eventos
 * Observabilidade (logs estruturados e métricas)

## Trade-offs e Limitações Conhecidas

- A indexação textual é síncrona no fluxo de escrita, priorizando simplicidade.
- Não foi implementado cache de busca para evitar complexidade prematura.
- Autenticação e autorização foram propositalmente omitidas por não fazerem parte do escopo do desafio.
- A busca textual não implementa stemming ou linguagem específica, utilizando os recursos nativos do MongoDB.

## Considerações Finais

Esta aplicação foi construída com foco em:

 * clareza arquitetural
 * facilidade de evolução
 * boas práticas de backend
 * separação explícita de responsabilidades

Cada decisão técnica foi pensada para refletir cenários reais de produção.