FROM node:20-alpine

WORKDIR /app

# Instala dependências primeiro (aproveita cache de camadas do Docker)
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

# --host 0.0.0.0: permite acessar o Vite de fora do container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173", "--strictPort"]
