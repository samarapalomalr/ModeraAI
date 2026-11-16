import ThemeToggle from "./ThemeToggle";
import { useTheme } from "../hooks/useTheme";

export default function AuthLayout({ title, subtitle, children, footer }) {
  const { theme, toggle } = useTheme();

  return (
    <div className="auth">
      <div className="auth-form-side">
        <div className="auth-top">
          <a href="#topo" className="nav-brand" onClick={() => (window.location.hash = "")}>
            <span className="nav-logo">🛡️</span> ModeraAI
          </a>
          <ThemeToggle theme={theme} onToggle={toggle} inline />
        </div>

        <div className="auth-box">
          <h1 className="auth-title">{title}</h1>
          <p className="auth-sub">{subtitle}</p>
          {children}
          <p className="auth-footer">{footer}</p>
        </div>
      </div>

      <aside className="auth-visual">
        <img src="/images/redes-sociales.jpg" alt="" />
        <div className="auth-visual-overlay">
          <h2>Moderação inteligente, em segundos.</h2>
          <p>Imagem, legenda e comentários analisados juntos pelo Google Gemini.</p>
        </div>
      </aside>
    </div>
  );
}
