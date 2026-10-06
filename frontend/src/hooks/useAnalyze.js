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
  const analyze = async (post_url) => {
    if (!post_url || post_url.trim() === "") {
      setError("⚠️ Informe uma URL válida");
      return;
    }

    const url = post_url.trim();

    setLoading(true);
    setError(null);
    setData(null);

    const maxAttempts = 2;
    let attempts = 0;

    while (attempts < maxAttempts) {
      try {
        const response = await api.post("/analyze", {
          post_url: url,
        });

        // -----------------------------
        // defensive validation
        // -----------------------------
        if (!response) {
          throw new Error("Sem resposta do servidor");
        }

        if (!response.data) {
          throw new Error("Resposta vazia da API");
        }

        if (!response.data.metrics) {
          throw new Error("Formato de resposta inválido");
        }

        // -----------------------------
        // success
        // -----------------------------
        setData(response.data);
        setLoading(false);
        return;

      } catch (err) {
        attempts++;

        console.warn(
          `[ANALYZE ERROR] tentativa ${attempts}/${maxAttempts}:`,
          err.message
        );

        // -----------------------------
        // You can still try again
        // -----------------------------
        if (attempts < maxAttempts) {
          setError("🔁 Servidor instável... tentando novamente");

          // Wait before retrying (prevents flooding in the backend)
          await sleep(2500);
          continue;
        }

        // -----------------------------
        // failed all attempts
        // -----------------------------
        setError(
          err.message ||
            "❌ Não foi possível processar o post no momento. Tente novamente."
        );

        setLoading(false);
        return;
      }
    }
  };

  // -----------------------------
  // RESET STATE
  // -----------------------------
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