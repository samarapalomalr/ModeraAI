# 🛡️ ModeraAI - Auditor e Moderador de Conteúdo com IA Multimodal

Trabalho prático desenvolvido para a disciplina de **Programação Web** do curso de Ciência da Computação da **Universidade Federal de Ouro Preto (UFOP)**.

### 👥 Integrantes do Grupo

- Ciro
- Estefanio
- Joao
- Samara

---

## 📌 Sobre o projeto

O **ModeraAI** é uma solução Full-Stack de Inteligência e Segurança Digital que utiliza IA Generativa e Visão Computacional para moderar e auditar publicações em redes sociais. Através de uma arquitetura baseada em FastAPI e React, a aplicação automatiza o ciclo completo desde a coleta de dados de uma publicação até a geração de relatórios de segurança e toxicidade. O sistema utiliza o **Google Gemini 2.5 Flash** para processar simultaneamente a imagem, a legenda e os comentários da publicação, garantindo uma análise contextual profunda sobre discursos de ódio, conteúdo ofensivo, sensacionalismo e adequação etária.

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

`Frontend (React - Vercel)` ➔ `Backend (FastAPI - Render)` ➔ `API de IA (Google Gemini)` ➔ `Coleta de dados (Apify)`

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
- Docker (ambiente de desenvolvimento)

### Backend

- Python
- FastAPI
- Render (deploy)

### Inteligência Artificial

- Google Gemini 2.5 Flash

### Coleta de Dados

- Apify

---

## 🌿 Branch `feat/docker`

> Esta seção descreve a branch `feat/docker` e pode ser removida do README depois que o Pull Request for aceito na `main`.

### Objetivo

Padronizar o ambiente de desenvolvimento do frontend para que **todos os devs rodem o projeto exatamente da mesma forma**, independentemente do sistema operacional ou da versão de Node instalada na máquina.

### O que mudou

| Arquivo                  | Mudança                                                                                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `docker-compose.yml`     | **Novo.** Sobe o frontend na porta `5173`, com o código montado por volume (hot reload) e o `node_modules` guardado em um volume do Docker.            |
| `frontend/Dockerfile`    | **Novo.** Imagem `node:20-alpine`. Ao subir, executa `npm install` e depois inicia o Vite com `--host 0.0.0.0`.                                        |
| `frontend/.dockerignore` | **Novo.** Evita enviar `node_modules`, `dist` e `.env` para o contexto de build.                                                                       |
| `.gitignore`             | Agora ignora `node_modules/`, `dist/`, `.env`, `backend/.env` e arquivos temporários de Python.                                                        |
| `frontend/node_modules`  | **Removido do versionamento** (cerca de 5 mil arquivos que estavam commitados). A pasta continua existindo localmente, mas o git não a acompanha mais. |
| `README.md`              | Documentação de como rodar com Docker.                                                                                                                 |

### O que **não** mudou

- Nenhum código do frontend (`src/`, `package.json`, `vite.config.js`) foi alterado.
- O backend **ainda não está no Docker**. Ele continua sendo executado separadamente e precisa estar em `http://localhost:8000`, que é a URL usada em `frontend/src/services/api.js`.

### Como testar esta branch (para quem vai revisar o PR)

O `git clone` baixa todas as branches, mas deixa ativa só a branch padrão (`main`). Enquanto o PR não for aceito, a `main` **não tem** o `docker-compose.yml`, então é preciso entrar na `feat/docker`. Escolha o caso que se aplica:

**Ainda não clonou o projeto: clone já na branch**

```bash
git clone -b feat/docker https://github.com/samarapalomalr/ModeraAI.git
cd ModeraAI
docker compose up --build
```

**Já tem o projeto clonado: troque de branch**

```bash
git fetch origin
git checkout feat/docker
docker compose up --build
```

(`git switch feat/docker` faz o mesmo que o `checkout`.) O `git fetch` é necessário para a sua máquina conhecer branches criadas depois do seu clone.

Quando aparecer `VITE ... ready` no terminal, abra http://localhost:5173. Se a página carregar, o ambiente está correto.

Para conferir em qual branch você está:

```bash
git branch        # a branch ativa aparece com *
git branch -a     # lista também as branches remotas (origin/...)
```

Para voltar para a `main`:

```bash
git checkout main
```

> Se você tiver alterações não commitadas, o git pode recusar a troca de branch. Faça commit ou use `git stash` antes.

### ⚠️ Aviso para quem já tem o projeto clonado

Depois que esta branch for aceita na `main`, ao fazer `git pull` o git **vai apagar o `node_modules` local**, porque esses arquivos eram versionados. Isso é esperado e não é erro. Depois do pull:

```bash
docker compose up --build
```

(ou `npm install` dentro de `frontend/`, para quem não usa Docker).

Quem estiver com uma branch aberta deve fazer `git merge main` nela depois que o Docker entrar. Se houver conflito envolvendo `node_modules`, aceite a remoção.

---

## 🐳 Como executar com Docker (recomendado)

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) ou Docker Engine com Compose v2 (Linux).
- O Docker Desktop precisa estar **aberto e com o status "Engine running"** antes de rodar os comandos.

### Passo a passo

```bash
# 1. Clone o repositório e entre na pasta
git clone https://github.com/samarapalomalr/ModeraAI.git
cd ModeraAI

# 2. Suba o ambiente
docker compose up --build
```

> **Enquanto o PR da `feat/docker` não for aceito**, o `git clone` simples traz a `main`, que ainda não tem o Docker. Nesse caso, clone direto na branch:
>
> ```bash
> git clone -b feat/docker https://github.com/samarapalomalr/ModeraAI.git
> ```
>
> ou, se já clonou, troque de branch com `git fetch origin` e `git checkout feat/docker`. Depois do merge na `main`, o clone simples funciona normalmente.

Na primeira execução o Docker baixa a imagem do Node e instala as dependências dentro do container, o que leva alguns minutos. Quando aparecer `VITE ... ready`, acesse:

- **Frontend:** http://localhost:5173

### Comandos úteis

| Comando                           | O que faz                                                                                  |
| --------------------------------- | ------------------------------------------------------------------------------------------ |
| `docker compose up`               | Sobe o ambiente (sem refazer a imagem).                                                    |
| `docker compose up --build`       | Sobe refazendo a imagem.                                                                   |
| `docker compose down`             | Para e remove os containers. **Mantém** o `node_modules`.                                  |
| `docker compose down -v`          | Para tudo e **apaga também o volume** do `node_modules` (a próxima subida reinstala tudo). |
| `docker compose logs -f frontend` | Acompanha os logs do frontend.                                                             |

### Conectando com o backend

O frontend roda no navegador e chama `http://localhost:8000`. Por isso, o backend pode estar em qualquer lugar (outro container ou direto com `uvicorn`), desde que:

1. Esteja acessível em `localhost:8000` (se for container, publique a porta com `-p 8000:8000` e use `--host 0.0.0.0` no uvicorn).
2. Permita CORS para `http://localhost:5173`.