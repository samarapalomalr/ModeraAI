import { useState } from "react";
import api from "../services/api";

// Cor do indicador conforme a classificação de risco
function riskTone(harm) {
  const h = String(harm || "").toLowerCase();
  if (h.includes("sem") || h === "baixo") return "ok";
  if (h === "moderado") return "warn";
  if (h === "alto" || h.includes("cr")) return "danger";
  return "";
}

function toxicityTone(score) {
  if (score < 25) return "ok";
  if (score < 60) return "warn";
  return "danger";
}

export default function ResultCard({ data }) {
  // 0 = proxy do backend, 1 = URL direta do CDN, 2 = indisponível
  const [imageStage, setImageStage] = useState(0);

  if (!data) return null;

  // A imagem passa pelo proxy do backend (o CDN do Instagram bloqueia hotlink).
  const proxySrc = data.display_url
    ? `${api.defaults.baseURL}/media?url=${encodeURIComponent(data.display_url)}`
    : null;
  const imageSrc = imageStage === 0 ? proxySrc : data.display_url;
  const hasImage = Boolean(data.display_url);
  const showImage = hasImage && imageStage < 2;

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

  const tox = toxicityScore === null ? "" : toxicityTone(toxicityScore);

  return (
    <div className="card result-card">
      <h2 className="result-title">Diagnóstico de Moderação</h2>

      {/* IMAGEM + RESUMO */}
      <div className="post-layout" style={hasImage ? undefined : { gridTemplateColumns: "1fr" }}>
        {showImage && (
          <img
            className="post-image"
            src={imageSrc}
            alt="Imagem do post analisado"
            referrerPolicy="no-referrer"
            onError={() => setImageStage((s) => s + 1)}
          />
        )}
        {hasImage && !showImage && <div className="post-image-fallback">🖼️ Imagem indisponível</div>}
        <div>
          <h3 className="section-title">Sobre o post</h3>
          <p className="summary">{summaryText}</p>
          <div className="badges" style={{ justifyContent: "flex-start", marginTop: 0 }}>
            <span className={`badge ${riskTone(harmClass)}`}>⚠️ Risco: {String(harmClass)}</span>
            {viralClass && <span className="badge">🔥 {String(viralClass)}</span>}
            <span className="badge">📌 {contentType}</span>
            <span className="badge">Faixa etária: {ageRating}</span>
            {tone && <span className="badge">Tom: {tone}</span>}
          </div>
        </div>
      </div>

      {/* MÉTRICAS */}
      <div className="metrics">
        <div className="metric-card">
          <div className="metric-title">Curtidas</div>
          <div className="metric-value">{metrics?.likes?.toLocaleString() || 0}</div>
        </div>
        <div className="metric-card">
          <div className="metric-title">Comentários</div>
          <div className="metric-value">{metrics?.comments?.toLocaleString() || 0}</div>
        </div>
        <div className="metric-card">
          <div className="metric-title">Toxicidade</div>
          <div className={`metric-value ${tox ? `tone-${tox}` : ""}`}>
            {toxicityScore === null ? "—" : `${toxicityScore.toFixed(1)}%`}
          </div>
          {toxicityScore !== null && (
            <div className="meter">
              <span className={`tone-${tox}`} style={{ width: `${toxicityScore}%` }} />
            </div>
          )}
        </div>
      </div>

      <hr className="divider" />

      {/* RELATÓRIO DE MODERAÇÃO */}
      <div className="section">
        <h3>📋 Relatório de Moderação</h3>
        <ul className="list">
          {moderationList.length > 0 ? (
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
        <h3>✅ Recomendações e Diretrizes</h3>
        <ul className="list recs">
          {recommendationsList.length > 0 ? (
            recommendationsList.map((item, index) => (
              <li key={index} style={{ animationDelay: `${(moderationList.length + index) * 0.1}s` }}>
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
