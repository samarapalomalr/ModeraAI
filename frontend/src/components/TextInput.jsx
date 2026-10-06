import { useState } from "react";

export default function TextInput({ onSubmit, loading }) {
  const [value, setValue] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!value.trim()) {
      alert("Por favor, insira uma URL válida");
      return;
    }

    onSubmit(value);
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h2 style={{ marginBottom: 10 }}>Analisar Post</h2>

      <p className="subtitle">
        Cole a URL de um post do Instagram para gerar insights com IA
      </p>

      <div className="input-group">
        <input
          type="text"
          placeholder="https://instagram.com/p/..."
          className="input"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={loading}
        />

        <button className="button button-neon" disabled={loading}>
          {loading ? "Analisando..." : "Analisar"}
        </button>
      </div>
    </form>
  );
}