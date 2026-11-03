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

    if (!url || url.trim() === "") {
      setError("⚠️ Informe uma URL válida");
      return;
    }

    const cleanUrl = url.trim();

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
        // Retry logic
        // -----------------------------
        if (attempts < maxAttempts) {
          setError("🔁 Servidor instável... tentando novamente");
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