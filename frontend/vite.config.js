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
    // Abre o navegador ao iniciar o dev server (desativado no Docker via VITE_OPEN_BROWSER=false)
    open: process.env.VITE_OPEN_BROWSER !== 'false',
    // Em Docker no Windows/macOS os eventos de arquivo nem sempre chegam ao container;
    // CHOKIDAR_USEPOLLING=true ativa polling para o hot reload funcionar.
    watch: {
      usePolling: process.env.CHOKIDAR_USEPOLLING === 'true',
    },
  },
});
