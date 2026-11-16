import Demo from "../components/Demo";
import ThemeToggle from "../components/ThemeToggle";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../hooks/useTheme";

const FEATURES = [
  {
    icon: "🖼️",
    title: "Análise multimodal",
    text: "Imagem, legenda e comentários são avaliados em conjunto pelo Google Gemini, com contexto completo.",
  },
  {
    icon: "☣️",
    title: "Índice de toxicidade",
    text: "Pontuação de 0 a 100 para discurso de ódio, assédio, ameaças e desinformação nociva.",
  },
  {
    icon: "🔞",
    title: "Classificação indicativa",
    text: "Faixa etária sugerida (Livre a 18+) seguindo critérios da classificação brasileira.",
  },
  {
    icon: "🚦",
    title: "Nível de risco",
    text: "De “Sem risco” a “Crítico”, para priorizar o que a moderação precisa olhar primeiro.",
  },
  {
    icon: "📈",
    title: "Métricas de engajamento",
    text: "Curtidas, comentários e potencial viral calculados automaticamente para cada post.",
  },
  {
    icon: "📋",
    title: "Relatório e diretrizes",
    text: "Pontos de atenção e recomendações práticas de moderação, prontos para ação.",
  },
];

const STEPS = [
  {
    n: "01",
    title: "Cole o link",
    text: "Informe a URL pública da publicação que deseja auditar.",
  },
  {
    n: "02",
    title: "Coletamos os dados",
    text: "Legenda, imagem e comentários recentes são extraídos via Apify.",
  },
  {
    n: "03",
    title: "A IA analisa",
    text: "O Gemini interpreta texto e imagem juntos, com regras estritas de moderação.",
  },
  {
    n: "04",
    title: "Receba o laudo",
    text: "Um diagnóstico claro, com risco, toxicidade, faixa etária e recomendações.",
  },
];

const STACK = [
  "React",
  "Vite",
  "FastAPI",
  "Python",
  "SQLite",
  "Google Gemini",
  "Apify",
  "Docker",
];

const CREDITS = [
  {
    label: "Digital media use — Rawpixel (CC0)",
    href: "https://commons.wikimedia.org/wiki/File:Digital_media_use.jpg",
  },
  {
    label: "Redes Sociales — Tracy Le Blanc (CC0)",
    href: "https://commons.wikimedia.org/wiki/File:Redes_Sociales.jpg",
  },
  {
    label: "The Earth at Night — NASA Earth Observatory (domínio público)",
    href: "https://commons.wikimedia.org/wiki/File:The_earth_at_night.jpg",
  },
];

export default function Landing() {
  const { theme, toggle } = useTheme();
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <>
      {/* NAVBAR */}
      <nav className="nav">
        <a href="#topo" className="nav-brand">
          <span className="nav-logo">🛡️</span> ModeraAI
        </a>
        <div className="nav-links">
          <a href="#recursos">Recursos</a>
          <a href="#como-funciona">Como funciona</a>
          <a href="#demo">Demonstração</a>
        </div>
        <div className="nav-actions">
          <ThemeToggle theme={theme} onToggle={toggle} inline />
          {isAuthenticated ? (
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <span
                style={{
                  fontSize: "0.9rem",
                  color: "var(--text-soft)",
                  fontWeight: 500,
                }}>
                👤 {user?.name?.split(" ")[0]}
              </span>
              <button
                type="button"
                className="button ghost"
                style={{ padding: "6px 14px", fontSize: "0.85rem" }}
                onClick={logout}>
                Sair
              </button>
            </div>
          ) : (
            <>
              <a href="#/login" className="nav-login">
                Entrar
              </a>
              <a href="#/cadastro" className="button nav-cta">
                Criar conta
              </a>
            </>
          )}
        </div>
      </nav>

      {/* HERO */}
      <header id="topo" className="l-hero">
        <div className="l-hero-text">
          <span className="pill">✨ Moderação com IA multimodal</span>
          <h1 className="l-title">
            Entenda o risco de qualquer post{" "}
            <span className="grad">em segundos</span>
          </h1>
          <p className="l-lead">
            O ModeraAI audita publicações em redes sociais combinando imagem,
            legenda e comentários, e entrega toxicidade, faixa etária e
            recomendações de moderação num único laudo.
          </p>
          <div className="l-cta">
            <a href="#demo" className="button">
              Experimentar grátis
            </a>
            <a href="#como-funciona" className="button ghost">
              Ver como funciona
            </a>
          </div>
          <div className="l-stats">
            <div>
              <strong>Instagram</strong>
              <span>hoje · TikTok e YouTube em breve</span>
            </div>
            <div>
              <strong>Segundos</strong>
              <span>por análise</span>
            </div>
            <div>
              <strong>0–100</strong>
              <span>índice de toxicidade</span>
            </div>
          </div>
        </div>

        <div className="l-hero-visual">
          <img
            src="/images/redes-sociales.jpg"
            alt="Pessoa segurando um celular com aplicativos de redes sociais"
          />
          <div className="float-card fc-1">
            <span className="fc-label">Toxicidade</span>
            <strong className="tone-ok">8%</strong>
            <div className="meter">
              <span className="tone-ok" style={{ width: "8%" }} />
            </div>
          </div>
          <div className="float-card fc-2">
            <span className="badge ok">⚠️ Risco: Baixo</span>
            <span className="badge">Faixa etária: Livre</span>
          </div>
        </div>
      </header>

      {/* PROBLEMA */}
      <section className="l-section">
        <div className="split">
          <img
            className="split-img"
            src="/images/earth-at-night.jpg"
            alt="Mapa da Terra à noite, com as luzes das cidades"
          />
          <div>
            <p className="eyebrow">O desafio</p>
            <h2 className="l-h2">
              Bilhões de publicações. Impossível revisar tudo na mão.
            </h2>
            <p className="l-p">
              O volume de conteúdo cresce todos os dias e a moderação manual não
              acompanha. Discurso de ódio, assédio e conteúdo inadequado passam
              despercebidos, e o contexto de uma imagem com legenda e
              comentários muda completamente o seu significado.
            </p>
            <p className="l-p">
              O ModeraAI automatiza a triagem com uma leitura contextual, para
              que as pessoas foquem nas decisões que realmente exigem julgamento
              humano.
            </p>
          </div>
        </div>
      </section>

      {/* RECURSOS */}
      <section id="recursos" className="l-section">
        <div className="l-head">
          <p className="eyebrow">Recursos</p>
          <h2 className="l-h2">Tudo o que a moderação precisa, num só laudo</h2>
        </div>
        <div className="grid-3">
          {FEATURES.map((f) => (
            <article key={f.title} className="feature">
              <div className="feature-icon">{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.text}</p>
            </article>
          ))}
        </div>
      </section>

      {/* COMO FUNCIONA */}
      <section id="como-funciona" className="l-section">
        <div className="l-head">
          <p className="eyebrow">Como funciona</p>
          <h2 className="l-h2">Do link ao diagnóstico em quatro passos</h2>
        </div>
        <div className="grid-4">
          {STEPS.map((s) => (
            <div key={s.n} className="step">
              <span className="step-n">{s.n}</span>
              <h3>{s.title}</h3>
              <p>{s.text}</p>
            </div>
          ))}
        </div>
      </section>

      {/* DEMO */}
      <section id="demo" className="l-section">
        <div className="l-head">
          <p className="eyebrow">Demonstração</p>
          <h2 className="l-h2">Teste com um post real</h2>
          <p className="l-p center">
            Cole o link de uma publicação pública e veja o laudo completo.
          </p>
        </div>
        <Demo />
      </section>

      {/* CTA FINAL */}
      <section className="l-section">
        <div className="cta-band">
          <h2>Pronto para auditar seu primeiro post?</h2>
          <p>Sem cadastro. Cole o link e receba o laudo em segundos.</p>
          <a href="#demo" className="button light">
            Começar agora
          </a>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="l-footer">
        <div className="l-footer-top">
          <span className="nav-brand">
            <span className="nav-logo">🛡️</span> ModeraAI
          </span>
          <span>Auditor e moderador de conteúdo com IA multimodal.</span>
        </div>
        <div className="credits">
          Imagens de domínio público / CC0 (Wikimedia Commons):{" "}
          {CREDITS.map((c, i) => (
            <span key={c.href}>
              <a href={c.href} target="_blank" rel="noreferrer">
                {c.label}
              </a>
              {i < CREDITS.length - 1 ? " · " : ""}
            </span>
          ))}
        </div>
      </footer>
    </>
  );
}
