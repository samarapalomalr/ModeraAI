import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      jsxRuntime: 'automatic', // 👈 Garante que a sintaxe JSX funciona sem precisar importar o React em todos os ficheiros
    }),
  ],
  server: {
    host: true, // Necessário para expor o servidor fora do container Docker
    port: 5173,
    open: !process.env.DOCKER, // Abre o navegador só fora do Docker
  },
});