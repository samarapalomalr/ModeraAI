import React, { useState } from "react";

feat/seletor-plataformas-e-erros
export default function TextInput({ onSubmit, loading }) {
  const [platform, setPlatform] = useState("instagram");
  const [url, setUrl] = useState("");

  const platforms = [
    { id: "instagram", name: "Instagram", placeholder: "https://instagram.com/p/..." },
    { id: "tiktok", name: "TikTok", placeholder: "https://www.tiktok.com/@usuario/video/..." },
    { id: "youtube", name: "YouTube", placeholder: "https://www.youtube.com/watch?v=..." },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url.trim()) return;
    onSubmit({ url, platform });

export default function TextInput({ onSubmit, loading, placeholder }) {
  const [value, setValue] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!value.trim()) {
      alert("Por favor, insira uma URL válida");
      return;
    }

    onSubmit(value.trim());
 main
  };

  const currentPlatform = platforms.find((p) => p.id === platform);

  return (
    <div className="card">
      {/* SELETOR DE PLATAFORMAS */}
      <div style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
        {platforms.map((p) => (
          <button
            key={p.id}
            type="button"
            onClick={() => setPlatform(p.id)}
            style={{
              flex: 1,
              padding: "8px 12px",
              borderRadius: "8px",
              border: platform === p.id ? "2px solid #2563eb" : "1px solid #cbd5e1",
              backgroundColor: platform === p.id ? "#eff6ff" : "#ffffff",
              color: platform === p.id ? "#1e40af" : "#475569",
              fontWeight: platform === p.id ? "600" : "normal",
              cursor: "pointer",
              transition: "all 0.2s"
            }}
          >
            {p.name}
          </button>
        ))}
      </div>

feat/seletor-plataformas-e-erros
      {/* MENSAGEM DE INSTRUÇÃO */}
      <p style={{ fontSize: "14px", color: "#64748b", marginBottom: "8px", textAlign: "left" }}>
        Cole o link do post da rede social que deseja analisar:

      <p className="subtitle">
        Cole a URL de um post para gerar informações sobre o conteúdo
main
      </p>

      {/* FORMULÁRIO DE ENTRADA */}
      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "8px" }}>
        <input
feat/seletor-plataformas-e-erros
          type="text"

          type="url"
          placeholder={placeholder || "https://..."}
 main
          className="input"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder={currentPlatform.placeholder}
          required
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
            outline: "none"
          }}
        />
 feat/seletor-plataformas-e-erros
        <button className="button" type="submit" disabled={loading}>


        <button className="button button-neon" disabled={loading || !value.trim()}>
 main
          {loading ? "Analisando..." : "Analisar"}
        </button>
      </form>
    </div>
  );
}