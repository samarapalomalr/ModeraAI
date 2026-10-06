export default function ResultCard({ data }) {
    if (!data) return null;
  
    const {
      metrics,
      engagement_score,
      viral_classification,
      content_type,
      sentiment,
      insights,
      recommendations,
    } = data;
  
    return (
      <div className="card result-card">
        <div className="result-header">
          <h2 style={{ textAlign: 'center', marginBottom: '24px' }}> Resultado da Análise</h2>
        </div>
  
        {/* METRICS  */}
        <div className="metrics">
          <div className="metric-card">
            <div className="metric-title">Likes</div>
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
            <div className="metric-title">Engajamento</div>
            <div className="metric-value">
              {engagement_score || 0}%
            </div>
          </div>
        </div>
  
        {}
        <div className="section" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', justifyContent: 'center', marginTop: '20px' }}>
          <span className="badge">
            🔥 {viral_classification?.toUpperCase()}
          </span>
          <span className="badge">
            📌 {content_type}
          </span>
          <span className="badge">
            🎭 {sentiment}
          </span>
        </div>
  
        <hr style={{ border: '0', borderTop: '1px solid #f1f5f9', margin: '30px 0' }} />
  
        {/* INSIGHTS */}
        <div className="section">
          <h3>Relatório de Moderação</h3>
          <ul className="list">
            {insights && insights.length > 0 ? (
              insights.map((item, index) => (
                <li key={index} style={{ animationDelay: `${index * 0.1}s` }}>
                  {item}
                </li>
              ))
            ) : (
              <li>Nenhum conteúdo disponível.</li>
            )}
          </ul>
        </div>
  
        {/* RECOMMENDATIONS */}
        <div className="section">
          <h3>Recomendações </h3>
          <ul className="list">
            {recommendations && recommendations.length > 0 ? (
              recommendations.map((item, index) => (
                <li 
                  key={index} 
                  style={{ animationDelay: `${((insights?.length || 0) + index) * 0.1}s` }}
                >
                  {item}
                </li>
              ))
            ) : (
              <li>Sem informações no momento.</li>
            )}
          </ul>
        </div>
      </div>
    );
  }