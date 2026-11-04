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
- SQLAlchemy + SQLite (histórico de auditorias)

### Inteligência Artificial
- Google Gemini

### Coleta de Dados
- Apify

### Infraestrutura
- Docker e Docker Compose
- sqlite-web (interface web do banco de dados)

---

## 🐳 Como rodar com Docker (recomendado)

Com o Docker, **frontend, backend e a interface do banco sobem juntos com um único comando**, sem instalar Python ou Node na sua máquina.

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) com Docker Compose v2 (`docker compose version`)
- Chave da API do **Google Gemini**: https://aistudio.google.com/app/apikey
- Token da API do **Apify**: https://console.apify.com/account/integrations

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/samarapalomalr/ModeraAI.git
cd ModeraAI

# 2. Crie o arquivo .env a partir do modelo
cp .env.example .env        # Windows (PowerShell): Copy-Item .env.example .env

# 3. Abra o .env e preencha GEMINI_API_KEY e APIFY_API_KEY

# 4. Suba tudo (a primeira vez demora por causa do build)
docker compose up --build
```

### Serviços disponíveis

| Serviço | URL | Descrição |
|---|---|---|
| Frontend (React + Vite) | http://localhost:5173 | Interface da aplicação |
| Backend (FastAPI) | http://localhost:8000 | API (documentação interativa em http://localhost:8000/docs) |
| sqlite-web | http://localhost:8080 | Interface web para visualizar e consultar o banco SQLite |

> As portas podem ser alteradas no `.env` (`FRONTEND_PORT`, `BACKEND_PORT`, `SQLITE_WEB_PORT`).

### Variáveis de ambiente (`.env`)

| Variável | Obrigatória | Descrição |
|---|---|---|
| `GEMINI_API_KEY` | ✅ | Chave da API do Google Gemini |
| `APIFY_API_KEY` | ✅ | Token da API do Apify |
| `GEMINI_MODEL` | ❌ | Modelo do Gemini (padrão: `gemini-2.5-flash`) |
| `FRONTEND_PORT` / `BACKEND_PORT` / `SQLITE_WEB_PORT` | ❌ | Portas expostas na sua máquina |
| `SQLITE_DB_FILE` | ❌ | Nome do arquivo do banco no volume Docker (padrão: `moderaai.db`) |
| `CHOKIDAR_USEPOLLING` | ❌ | `true` no Windows/macOS para o hot reload do frontend funcionar; pode ser `false` no Linux |

⚠️ **O arquivo `.env` contém chaves secretas e nunca deve ser versionado.** Apenas o `.env.example` vai para o GitHub.

### Comandos úteis

```bash
docker compose up -d --build        # sobe em segundo plano
docker compose logs -f backend      # acompanha os logs de um serviço
docker compose ps                   # status dos containers
docker compose down                 # para e remove os containers (mantém o banco)
docker compose down -v              # ⚠️ também apaga o volume do banco de dados

# Popula o banco com auditorias de teste (sem gastar cota das APIs)
docker compose exec backend python seed.py
```

### 🗄️ Banco de dados

O projeto usa **SQLite** (via SQLAlchemy). No Docker, o arquivo do banco fica em um **volume nomeado** (`sqlite_data`), então os dados persistem entre reinicializações. Para explorar as tabelas (`audits`), rodar consultas SQL ou exportar dados, acesse o **sqlite-web** em http://localhost:8080.

> A interface do banco não possui autenticação, por isso é exposta apenas em `127.0.0.1`.

### 🔧 Solução de problemas

- **`Defina GEMINI_API_KEY no arquivo .env`**: o `.env` não existe ou está com a chave vazia. Veja o passo 2 e 3.
- **Porta já em uso**: altere a porta correspondente no `.env`.
- **Instalei uma dependência nova (`requirements.txt` ou `package.json`)**: rode `docker compose up --build -V` para reconstruir as imagens e renovar o `node_modules` do container.
- **Hot reload do frontend não funciona (Windows/macOS)**: confirme `CHOKIDAR_USEPOLLING=true` no `.env`.

---

## ▶️ Como rodar o projeto localmente (sem Docker)

Você precisará de **dois terminais**: um para o Backend e outro para o Frontend. Requer Python 3.10+ e Node.js 18+.

### 🔹 1. Clone o repositório e configure o `.env`
```bash
git clone https://github.com/samarapalomalr/ModeraAI.git
cd ModeraAI
cp .env.example .env   # preencha GEMINI_API_KEY e APIFY_API_KEY
```

### 🔹 2. Terminal 1: Backend (FastAPI)
```bash
cd backend

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
# .\venv\Scripts\Activate      # Windows (PowerShell)

# Instale as dependências e inicie o servidor (permaneça na pasta backend/)
pip install -r requirements.txt
uvicorn app.main:app --reload
```
O backend estará em http://localhost:8000. Sem Docker, o banco é criado automaticamente em `backend/moderaai.db`.

### 🔹 3. Terminal 2: Frontend (React / Vite)
```bash
cd frontend
npm install
npm run dev
```
O frontend estará em http://localhost:5173.
