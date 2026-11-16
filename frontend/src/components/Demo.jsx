import { useState } from "react";
import { useAnalyze } from "../hooks/useAnalyze";
import Loader from "./Loader";
import ResultCard from "./ResultCard";
import TextInput from "./TextInput";

const PLATFORMS = [
  {
    id: "instagram",
    name: "Instagram",
    placeholder: "https://www.instagram.com/p/...",
  },
  {
    id: "tiktok",
    name: "TikTok",
    placeholder: "https://www.tiktok.com/@usuario/video/...",
    soon: true,
  },
  {
    id: "youtube",
    name: "YouTube",
    placeholder: "https://www.youtube.com/watch?v=...",
    soon: true,
  },
];

export default function Demo() {
  const [platform, setPlatform] = useState("instagram");
  const { analyze, data, loading, error, reset } = useAnalyze();
  const selectedPlatform = PLATFORMS.find((p) => p.id === platform);

  return (
    <div className="demo">
      <div className="tabs">
        {PLATFORMS.map((p) => (
          <button
            key={p.id}
            type="button"
            className={`tab ${platform === p.id ? "active" : ""}`}
            onClick={() => setPlatform(p.id)}
            disabled={loading || p.soon}
            title={p.soon ? "Em breve" : undefined}>
            {p.name}
            {p.soon ? " · em breve" : ""}
          </button>
        ))}
      </div>

      {/* Só reinicia ao voltar do resultado; trocar de plataforma mantém o texto digitado */}
      <TextInput
        key={data ? "analisado" : "novo"}
        placeholder={selectedPlatform?.placeholder}
        onSubmit={(url) => analyze({ url, platform })}
        loading={loading}
      />

      {error && !loading && (
        <div className="card error-card">
          <span style={{ fontSize: 20 }}>⚠️</span>
          <div>
            <h4>Não foi possível concluir a análise</h4>
            <p>{error}</p>
          </div>
        </div>
      )}

      {loading && <Loader />}

      {data && !loading && (
        <>
          <ResultCard data={data} platform={platform} />
          <div className="actions">
            <button className="button ghost" onClick={reset}>
              Analisar novo post
            </button>
          </div>
        </>
      )}
    </div>
  );
}
