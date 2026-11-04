import axios from "axios";

// URL do backend: definida via VITE_API_URL (docker-compose) ou localhost por padrão
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const wakeUpBackend = async () => {
  try {
    await api.get("/");
  } catch (err) {
    console.warn("Aguardando o backend responder...", err.message);
  }
};

export default api;
