import { useState } from "react";

export default function TextInput({ onSubmit, loading, placeholder }) {
  const [value, setValue] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!value.trim()) {
      alert("Por favor, insira uma URL válida");
      return;
    }

    onSubmit(value.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h2 style={{ marginBottom: 10 }}>Analisar Post</h2>

      <p className="subtitle">
        Cole a URL de um post para gerar informações sobre o conteúdo
      </p>

      <div className="input-group">
        <input
          type="url"
          placeholder={placeholder || "https://..."}
          className="input"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={loading}
        />

        <button className="button button-neon" disabled={loading || !value.trim()}>
          {loading ? "Analisando..." : "Analisar"}
        </button>
      </div>
    </form>
  );
}