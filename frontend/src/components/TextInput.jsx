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
      <p className="input-label">Cole o link do post que deseja analisar:</p>
      <form onSubmit={handleSubmit} className="input-group">
        <input
          type="text"
          className="input"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={placeholder || "https://..."}
          required
        />
        <button className="button" type="submit" disabled={loading || !value.trim()}>
          {loading ? "Analisando..." : "Analisar"}
        </button>
      </form>
    </div>
  );
}
