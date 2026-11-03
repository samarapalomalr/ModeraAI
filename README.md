# 🛡️ ModeraAI - Auditor e Moderador de Conteúdo com IA Multimodal

Trabalho prático desenvolvido para a disciplina de **Programação Web** do curso de Ciência da Computação da **Universidade Federal de Ouro Preto (UFOP)**.

### 👥 Integrantes do Grupo 
- Ciro Junio 
- Estefanio Miko
- Joao Pedro
- Samara Paloma

---

## 📌 Sobre o projeto

O **ModeraAI** é uma solução Full-Stack de Inteligência e Segurança Digital que utiliza IA Generativa e Visão Computacional para moderar e auditar publicações em redes sociais e plataformas. Através de uma arquitetura baseada em FastAPI e React, a aplicação automatiza o ciclo completo desde a coleta de dados de uma publicação até a geração de relatórios de segurança e toxicidade. O sistema utiliza o **Google Gemini** para processar simultaneamente a imagem, a legenda e os comentários da publicação, garantindo uma análise contextual profunda sobre discursos de ódio, conteúdo ofensivo, sensacionalismo e adequação etária.

---

## 🧠 Funcionalidades

O fluxo de dados foi projetado para ser linear, seguro e eficiente:

1. **Entrada:** O usuário insere a URL de um post do Instagram na interface web.
2. **Coleta (Scraping):** O backend via FastAPI aciona a API do Apify para extrair os dados da publicação (legenda, URL da imagem e comentários recentes).
3. **Processamento Multimodal:** A legenda, os comentários e o elemento visual do post são enviados ao Google Gemini. A IA analisa o conteúdo visual e textual de forma integrada.
4. **Inteligência de Moderação:** O sistema calcula o **Toxicity & Harm Score** (Score de Toxicidade e Risco), classifica categorias sensíveis (discurso de ódio, violência, profanação, assédio) e sugere a indicação etária.
5. **Entrega:** O frontend renderiza um dashboard com alertas visuais de segurança, trechos destacados de comentários ofensivos, justificativas da IA e recomendações de moderação.

---

## 🏗️ Arquitetura do Sistema

A aplicação segue uma arquitetura cliente-servidor desacoplada:

`Frontend (React - Vercel)` ➔ `Backend (FastAPI)` ➔ `API de IA (Google Gemini)` ➔ `Coleta de dados (Apify)`

---

### 🔄 Fluxo da Aplicação

1. O usuário insere a URL de um post do Instagram no frontend.
2. O frontend envia a requisição de análise para o backend.
3. O backend coleta mídias, legenda e comentários via Apify.
4. Os dados coletados são submetidos ao Google Gemini com diretrizes estritas de moderação.
5. A IA gera o diagnóstico de segurança, pontuação de toxicidade e recomendações.
6. O backend estrutura os dados retornados.
7. O frontend exibe os alertas e métricas no dashboard de moderação.

---

## ⚙️ Tecnologias Utilizadas

### Frontend
- React
- Vite
- Axios
- Vercel (deploy)

### Backend
- Python
- FastAPI

### Inteligência Artificial
- Google Gemini

### Coleta de Dados
- Apify

---

## 📁 Estrutura do projeto

```
ModeraAI/
├── docker-compose.yml        # Sobe frontend + backend + interface do banco
├── .env.example              # Modelo de variáveis (versionado)
├── .env                      # Variáveis reais (NÃO versionado)
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── seed.py               # Popula o banco com dados de teste
│   └── app/
│       ├── main.py           # Criação da app FastAPI
│       ├── api/              # Camada de apresentação (rotas HTTP)
│       │   ├── router.py
│       │   ├── deps.py       # Injeção de dependências
│       │   └── routes/       # health, analyze, audits
│       ├── schemas/          # DTOs Pydantic (request/response)
│       ├── services/         # Regras de negócio e integrações (Gemini, Apify)
│       ├── repositories/     # Acesso a dados (SQLAlchemy)
│       ├── models/           # Entidades do banco
│       ├── core/             # Config, conexão com o banco, exceções
│       └── utils/            # Funções auxiliares (texto, validadores)
└── frontend/
    ├── Dockerfile
    └── src/                  # components, hooks, pages, services
```

Fluxo entre as camadas do backend: `api (rotas)` ➔ `services` ➔ `repositories` ➔ `models/banco`.

---

## 🐳 Como rodar com Docker (recomendado)

**Pré-requisitos:** [Docker](https://docs.docker.com/get-docker/) e Docker Compose v2.

```bash
# 1. Clone o repositório
git clone https://github.com/samarapalomalr/ModeraAI.git
cd ModeraAI

# 2. Crie o arquivo .env a partir do modelo e preencha as chaves de API
cp .env.example .env
#    -> edite o .env e informe GEMINI_API_KEY e APIFY_API_KEY

# 3. Suba todos os serviços
docker compose up --build
```

| Serviço | URL | Descrição |
|---|---|---|
| Frontend (React/Vite) | http://localhost:5173 | Interface da aplicação |
| Backend (FastAPI) | http://localhost:8000 | API (docs em http://localhost:8000/docs) |
| sqlite-web | http://localhost:8080 | Interface web do banco SQLite |

As portas e demais configurações podem ser alteradas no `.env`.

### Comandos úteis

```bash
docker compose up -d                 # sobe em segundo plano
docker compose logs -f backend       # acompanha os logs do backend
docker compose down                  # para os containers (mantém o banco)
docker compose down -v               # para e APAGA o volume do banco
docker compose exec backend python seed.py   # popula o banco com dados de teste
```

> O banco SQLite fica no volume Docker `sqlite_data` e persiste entre execuções.
> Alterações no código do backend e do frontend são recarregadas automaticamente (hot reload).

### Variáveis de ambiente

| Variável | Descrição | Padrão |
|---|---|---|
| `GEMINI_API_KEY` | Chave da API do Google Gemini (**obrigatória**) | - |
| `APIFY_API_KEY` | Token da API do Apify (**obrigatória**) | - |
| `GEMINI_MODEL` | Modelo do Gemini | `gemini-2.5-flash` |
| `DEBUG` | Modo debug do backend | `true` |
| `CORS_ORIGINS` | Origens permitidas (separadas por vírgula) | `http://localhost:5173` |
| `SQLITE_DB_FILE` | Nome do arquivo do banco no volume | `moderaai.db` |
| `BACKEND_PORT` / `FRONTEND_PORT` / `SQLITE_WEB_PORT` | Portas expostas no host | `8000` / `5173` / `8080` |
| `VITE_API_URL` | URL do backend vista pelo navegador | `http://localhost:8000` |

⚠️ **Nunca versione o `.env`** — ele contém chaves secretas. Apenas o `.env.example` vai para o GitHub.

---

## ▶️ Como rodar localmente (sem Docker)

Abra **dois terminais separados**: um para o Backend e outro para o Frontend.
Na raiz do projeto, crie o `.env` (`cp .env.example .env`) e copie-o também para `backend/.env`
(o backend lê o `.env` da pasta onde é executado).

### Terminal 1: Backend (FastAPI)

```bash
cd backend

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
# .\venv\Scripts\Activate      # Windows (PowerShell)

pip install -r requirements.txt
uvicorn app.main:app --reload
```

O backend estará em http://localhost:8000. Sem `DATABASE_URL`, o banco é o arquivo local `backend/moderaai.db`.

### Terminal 2: Frontend (React / Vite)

```bash
cd frontend
npm install
npm run dev
```

O frontend estará em http://localhost:5173.
