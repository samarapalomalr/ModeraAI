import React, { useState } from "react";
import TextInput from "../components/TextInput";
import ResultCard from "../components/ResultCard";
import Loader from "../components/Loader";
import { useAnalyze } from "../hooks/useAnalyze";

const PLATFORMS = [
  { id: "instagram", name: "Instagram", placeholder: "https://www.instagram.com/p/..." },
  { id: "tiktok", name: "TikTok", placeholder: "https://www.tiktok.com/@usuario/video/..." },
  { id: "youtube", name: "YouTube", placeholder: "https://www.youtube.com/watch?v=..." },
];

export default function Home() {
  const [platform, setPlatform] = useState("instagram");
  const { analyze, data, loading, error, reset } = useAnalyze();

  const selectedPlatform = PLATFORMS.find((p) => p.id === platform);

  const handleAnalyze = (url) => {
    analyze({ url, platform });
  };

  return (
    <div className="container">
      {/* HEADER */}
      <div style={{ marginBottom: 30, textAlign: "center" }}>
        <h1 className="title">ModeraAI</h1>
        <p className="subtitle" style={{ color: "#64748b", marginTop: 8 }}>
          Auditor e moderador inteligente para Instagram, TikTok e YouTube.
        </p>
      </div>

      {/* SELETOR DE PLATAFORMA */}
      <div
        style={{
          display: "flex",
          gap: 8,
          marginBottom: 16,
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        {PLATFORMS.map((p) => (
          <button
            key={p.id}
            type="button"
            onClick={() => setPlatform(p.id)}
            disabled={loading}
            style={{
              padding: "8px 16px",
              borderRadius: 8,
              border: platform === p.id ? "2px solid #2563eb" : "1px solid #cbd5e1",
              backgroundColor: platform === p.id ? "#eff6ff" : "#ffffff",
              color: platform === p.id ? "#1e40af" : "#475569",
              fontWeight: platform === p.id ? 600 : "normal",
              cursor: loading ? "not-allowed" : "pointer",
              transition: "all 0.2s",
            }}
          >
            {p.name}
          </button>
        ))}
      </div>

      {/* INPUT (só reinicia ao voltar do resultado; trocar de plataforma mantém o texto digitado) */}
      <TextInput
        key={data ? "analisado" : "novo"}
        placeholder={selectedPlatform?.placeholder}
        onSubmit={handleAnalyze}
        loading={loading}
      />

      {/* MENSAGEM DE ERRO AMIGÁVEL */}
      {error && !loading && (
        <div
          className="card"
          style={{
            marginTop: 20,
            backgroundColor: "#fef2f2",
            borderLeft: "4px solid #ef4444",
            padding: "16px 20px",
          }}
        >
          <div style={{ display: "flex", alignItems: "flex-start", gap: "12px" }}>
            <span style={{ fontSize: "20px" }}>⚠️</span>
            <div>
              <h4 style={{ margin: 0, color: "#991b1b", fontWeight: 600, fontSize: "15px" }}>
                Não foi possível concluir a análise
              </h4>
              <p style={{ margin: "4px 0 0 0", color: "#b91c1c", fontSize: "14px", lineHeight: 1.4 }}>
                {error}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* LOADING */}
      {loading && <Loader />}

      {/* RESULT */}
      {data && !loading && (
        <>
          <ResultCard data={data} platform={platform} />
          <div style={{ marginTop: 24, textAlign: "center" }}>
            <button className="button" onClick={reset}>
              Analisar novo post
            </button>
          </div>
        </>
      )}
    </div>
  );
}
