import axios from "axios";

// 🌐 Configuração da URL Base do Backend
// Utiliza variável de ambiente para produção ou localhost como fallback em desenvolvimento
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// -----------------------------
// UTILITÁRIO DE ESPERA
// -----------------------------
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// -----------------------------
// ⚡ HEALTHCHECK / WAKE UP BACKEND
// -----------------------------
export const wakeUpBackend = async () => {
  try {
    console.log("🔄 Verificando conexão com o backend ModeraAI...");

    await fetch(`${BASE_URL}/`, {
      method: "GET",
    });

    console.log("✅ Backend ModeraAI ativo e respondendo");
  } catch (err) {
    console.warn("⚠️ Servidor ainda inicializando...");
  }
};

// -----------------------------
// INTERCEPTOR DE RESPOSTA E TRATAMENTO DE ERROS
// -----------------------------
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config;

    if (!config._retryCount) {
      config._retryCount = 0;
    }

    // 🔁 Tentativa de reconexão automática (Retry)
    if (
      config._retryCount < 2 &&
      (!error.response || error.code === "ECONNABORTED")
    ) {
      config._retryCount++;

      console.warn(
        `🔁 Tentativa ${config._retryCount} de 2: aguardando resposta da API...`
      );

      await sleep(2000);
      return api(config);
    }

    // 🔴 Tratamento de erro quando há resposta do servidor
    if (error.response) {
      console.error("[ERRO NA API MODERAAI]", {
        status: error.response.status,
        data: error.response.data,
      });

      const message =
        error.response.data?.detail ||
        error.response.data?.message ||
        "Erro ao processar requisição no servidor";

      throw new Error(message);
    }

    // 🌐 Tratamento de erro de rede ou timeout
    if (error.request) {
      console.error("[ERRO DE REDE]", error.request);

      throw new Error(
        "O servidor de moderação demorou a responder. Tente novamente em instantes."
      );
    }

    // ⚠️ Erro genérico/inesperado
    console.error("[ERRO INESPERADO]", error.message);

    throw new Error("Ocorreu um erro inesperado ao realizar a análise.");
  }
);

export default api;