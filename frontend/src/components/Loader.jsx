export default function Loader() {
  return (
    <div className="card loader-card">
      <div className="spinner" />
      <p className="loader-highlight">Analisando post com o Google Gemini...</p>
      <p className="subtitle">
        Avaliando imagem, legenda e comentários. Isso pode levar alguns segundos.
      </p>
    </div>
  );
}
