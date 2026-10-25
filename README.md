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

## ▶️ Como rodar o projeto localmente

Para rodar a aplicação em sua máquina, você precisará abrir **dois terminais separados**: um dedicado ao Backend e outro ao Frontend.

### 🔹 1. Clone o repositório
```bash
git clone [https://github.com/samarapalomalr/ModeraAI.git](https://github.com/samarapalomalr/ModeraAI.git)
cd ModeraAI

# Terminal 1: Backend (FastAPI)

# 1. Entre na pasta do backend
cd backend

# 2. Crie e ative o ambiente virtual
python -m venv venv
# No Linux/macOS:
source venv/bin/activate
# No Windows (PowerShell):
# .\venv\Scripts\Activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor FastAPI (permaneça na pasta backend/)
uvicorn app.main:app --reload

# O backend estará rodando em http://localhost:8000.

 Terminal 2: Frontend (React / Vite)

# 1. Navegue até a pasta do frontend em outro terminal
cd frontend

# 2. Instale as dependências
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev

# O frontend estará rodando em http://localhost:5173.
http://localhost:5173

🔹 5. Acesso ao sistema em produção

