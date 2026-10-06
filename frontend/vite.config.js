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
    port: 5173,
    open: true, // Abre o navegador automaticamente ao iniciar o dev server
  },
});