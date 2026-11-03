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
      <div style={{ marginBottom: 32, textAlign: "center" }}>
        <h1 className="title">ModeraAI</h1>
        <p className="subtitle">
          Análise inteligente de conteúdo em redes sociais
        </p>
      </div>

      {/* PLATFORM SELECTOR */}
      <div className="platform-selector" style={{ marginBottom: 20 }}>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", justifyContent: "center" }}>
          {PLATFORMS.map((p) => (
            <button
              key={p.id}
              type="button"
              onClick={() => setPlatform(p.id)}
              className={`platform-chip ${platform === p.id ? "active" : ""}`}
              disabled={loading}
            >
              {p.name}
            </button>
          ))}
        </div>
      </div>

      {/* INPUT */}
      <TextInput
        key={`${platform}-${data ? "analisado" : "novo"}`}
        placeholder={selectedPlatform?.placeholder}
        platform={platform}
        onSubmit={handleAnalyze}
        loading={loading}
      />

      {/* ERROR */}
      {error && (
        <div className="card" style={{ marginTop: 20 }}>
          <p style={{ color: "#ef4444", margin: 0 }}>❌ {error}</p>
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