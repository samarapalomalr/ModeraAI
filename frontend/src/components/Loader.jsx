import React, { useState } from "react";

export default function Loader() {
  return (
    <div className="card" style={{ textAlign: "center", padding: "40px" }}>
      <p className="loader-highlight">
        🛡️ Analisando post com o Google Gemini...
      </p>
      <p className="subtitle" style={{ marginBottom: 0 }}>
        Avaliando imagens, vídeos, legenda e comentários. Isso pode levar alguns segundos.
      </p>
    </div>
  );
}