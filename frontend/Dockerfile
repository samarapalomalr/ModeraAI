# Imagem de desenvolvimento do frontend (React + Vite)
FROM node:20-alpine

WORKDIR /app

EXPOSE 5173

# As dependências são instaladas ao subir o container (o código vem por volume).
# --host 0.0.0.0 é necessário para o Vite ficar acessível fora do container.
CMD ["sh", "-c", "npm install && npm run dev -- --host 0.0.0.0"]
