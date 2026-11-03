import { useState } from "react";
import api from "../services/api";

export function useAnalyze() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  // ANALYZE
  const analyze = async (input) => {
    // Trata se o input veio como string ou como objeto { url, platform }
    const rawUrl = typeof input === "object" ? input?.url : input;
    const platform = typeof input === "object" ? input?.platform : "instagram";

    // Validação da URL
    if (!rawUrl || typeof rawUrl !== "string" || rawUrl.trim() === "") {
      setError("⚠️ Informe uma URL válida");
      return;
    }

    const url = rawUrl.trim();

    setLoading(true);
    setError(null);
    setData(null);

    const maxAttempts = 2;
    let attempts = 0;

    while (attempts < maxAttempts) {
      try {
        const response = await api.post("/analyze", {
          post_url: url,
          platform: platform,
        });

        // defensive validation
        if (!response) {
          throw new Error("Sem resposta do servidor");
        }

        if (!response.data) {
          throw new Error("Resposta vazia da API");
        }

        if (!response.data.metrics) {
          throw new Error("Formato de resposta inválido");
        }

        // success
        setData(response.data);
        setLoading(false);
        return;

      } catch (err) {
        attempts++;

        console.warn(
          `[ANALYZE ERROR] tentativa ${attempts}/${maxAttempts}:`,
          err.message
        );

        if (attempts < maxAttempts) {
          setError("⚠️ Servidor instável... tentando novamente");
          await sleep(2500);
          continue;
        }

        // Exibe a mensagem amigável vinda do backend ou a mensagem genérica
        const errorMessage =
          err.response?.data?.detail ||
          err.response?.data?.message ||
          err.message ||
          "❌ Não foi possível processar o post no momento. Tente novamente.";

        setError(errorMessage);
      }

      setLoading(false);
      return;
    }
  };

  // RESET STATE
  const reset = () => {
    setData(null);
    setError(null);
    setLoading(false);
  };

  return {
    analyze,
    data,
    loading,
    error,
    reset,
  };
}