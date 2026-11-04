export default function ResultCard({ data }) {
  if (!data) return null;

  const metrics = data.metrics;

  // Toxicidade real (estimada pela IA, 0-100). Nunca usa engagement_score.
  const rawToxicity = data.toxicity_score;
  const hasToxicity = rawToxicity !== null && rawToxicity !== undefined && !Number.isNaN(Number(rawToxicity));
  const toxicityScore = hasToxicity ? Math.min(Math.max(Number(rawToxicity), 0), 100) : null;

  const harmClass = data.harm_classification || "Indeterminado";
  const viralClass = data.viral_classification;
  const contentType = data.content_category || data.content_type || "Geral";
  const ageRating = data.age_rating || "Indeterminado";
  const tone = data.sentiment;

  const summaryText = data.summary || "Resumo indisponível.";
  const moderationList = data.moderation_report || data.insights || [];
  const recommendationsList = data.recommendations || [];

  return (
    <div className="card result-card">
      <div className="result-header">
        <h2 style={{ textAlign: "center", marginBottom: "24px" }}>
          Diagnóstico de Moderação
        </h2>
      </div>

      {/* MÉTRICAS */}
      <div className="metrics">
        <div className="metric-card">
          <div className="metric-title">Curtidas</div>
          <div className="metric-value">
            {metrics?.likes?.toLocaleString() || 0}
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-title">Comentários</div>
          <div className="metric-value">
            {metrics?.comments?.toLocaleString() || 0}
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-title">Toxicidade</div>
          <div className="metric-value">
            {toxicityScore === null ? "—" : `${toxicityScore.toFixed(1)}%`}
          </div>
        </div>
      </div>

      {/* BADGES */}
      <div
        className="section"
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "10px",
          justifyContent: "center",
          marginTop: "20px",
        }}
      >
        <span className="badge">⚠️ Risco: {String(harmClass).toUpperCase()}</span>
        {viralClass && <span className="badge">🔥 {String(viralClass).toUpperCase()}</span>}
        <span className="badge">📌 {contentType}</span>
        <span className="badge">Faixa Etária: {ageRating}</span>
        {tone && <span className="badge">Tom: {tone}</span>}
      </div>

      <hr style={{ border: "0", borderTop: "1px solid #f1f5f9", margin: "30px 0" }} />

      {/* RESUMO DO POST */}
      <div className="section" style={{ textAlign: "left", marginBottom: "24px" }}>
        <h3 style={{ marginBottom: "8px", color: "#1e293b" }}>📌 Sobre o Post</h3>
        <p style={{ color: "#475569", lineHeight: "1.6", margin: 0 }}>
          {summaryText}
        </p>
      </div>

      {/* RELATÓRIO DE MODERAÇÃO */}
      <div className="section">
        <h3>📋 Relatório de Moderação</h3>
        <ul className="list">
          {moderationList && moderationList.length > 0 ? (
            moderationList.map((item, index) => (
              <li key={index} style={{ animationDelay: `${index * 0.1}s` }}>
                {item}
              </li>
            ))
          ) : (
            <li>Nenhum ponto crítico detectado na análise.</li>
          )}
        </ul>
      </div>

      {/* RECOMENDAÇÕES */}
      <div className="section">
        <h3>Recomendações e Diretrizes</h3>
        <ul className="list">
          {recommendationsList && recommendationsList.length > 0 ? (
            recommendationsList.map((item, index) => (
              <li
                key={index}
                style={{
                  animationDelay: `${((moderationList?.length || 0) + index) * 0.1}s`,
                }}
              >
                {item}
              </li>
            ))
          ) : (
            <li>Sem recomendações no momento.</li>
          )}
        </ul>
      </div>
    </div>
  );
}