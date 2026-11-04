import { useState } from "react";
import api from "../services/api";

export function useAnalyze() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  // -----------------------------
  // ANALYZE
  // -----------------------------
  const analyze = async (input) => {
    // Suporta tanto string direta quanto o objeto { url, platform } vindo do Home.jsx
    let url = "";
    let platform = "instagram";

    if (typeof input === "object" && input !== null) {
      url = input.url || "";
      platform = input.platform || "instagram";
    } else {
      url = input || "";
    }

    const cleanUrl = typeof url === "string" ? url.trim() : "";

    if (!cleanUrl) {
      setError("⚠️ Informe uma URL válida");
      return;
    }

    setLoading(true);
    setError(null);
    setData(null);

    const maxAttempts = 2;
    let attempts = 0;

    while (attempts < maxAttempts) {
      try {
        const response = await api.post("/analyze", {
          post_url: cleanUrl,
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

        // Erros 4xx (ex.: URL inválida) são do usuário: repetir não adianta
        const status = err.response?.status;
        const isClientError = status >= 400 && status < 500;

        // -----------------------------
        // Retry logic
        // -----------------------------
        if (!isClientError && attempts < maxAttempts) {
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
        setLoading(false);
        return;
      }
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
