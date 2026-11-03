import axios from "axios";

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
