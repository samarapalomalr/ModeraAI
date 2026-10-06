export default function ResultCard({ data }) {
  if (!data) return null;

  const metrics = data.metrics;
  const toxicityScore = data.toxicity_score ?? data.engagement_score ?? 0;
  const harmClass = data.harm_classification || data.viral_classification || "Sem Risco";
  const contentType = data.content_category || data.content_type || "Geral";
  const ageRating = data.age_rating || data.sentiment || "Livre";

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
            {toxicityScore}%
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
        <span className="badge">
          ⚠️ {String(harmClass).toUpperCase()}
        </span>
        <span className="badge">
          📌 {contentType}
        </span>
        <span className="badge">
          Faixa Etária: {ageRating}
        </span>
      </div>

      <hr style={{ border: "0", borderTop: "1px solid #f1f5f9", margin: "30px 0" }} />

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