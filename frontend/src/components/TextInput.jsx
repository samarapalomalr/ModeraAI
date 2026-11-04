import React, { useState } from "react";

export default function TextInput({ onSubmit, loading, placeholder }) {
  const [value, setValue] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!value.trim()) return;
    onSubmit(value.trim());
  };

  return (
    <div className="card">
      {/* MENSAGEM DE INSTRUÇÃO */}
      <p className="subtitle" style={{ marginBottom: "12px", textAlign: "left" }}>
        Cole o link do post da rede social que deseja analisar:
      </p>

      {/* FORMULÁRIO DE ENTRADA */}
      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "8px" }}>
        <input
          type="text"
          className="input"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={placeholder || "https://..."}
          required
          style={{ flex: 1 }}
        />

        <button className="button" type="submit" disabled={loading || !value.trim()}>
          {loading ? "Analisando..." : "Analisar"}
        </button>
      </form>
    </div>
  );
}
