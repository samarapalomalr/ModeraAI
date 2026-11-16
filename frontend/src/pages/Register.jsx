import { useState } from "react";
import AuthLayout from "../components/AuthLayout";
import Field from "../components/Field";
import { useAuth } from "../context/AuthContext";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function passwordStrength(pw) {
  let score = 0;
  if (pw.length >= 8) score++;
  if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) score++;
  if (/\d/.test(pw)) score++;
  if (/[^A-Za-z0-9]/.test(pw)) score++;
  return score; // 0-4
}

const STRENGTH = [
  { label: "Muito fraca", tone: "danger" },
  { label: "Fraca", tone: "danger" },
  { label: "Razoável", tone: "warn" },
  { label: "Boa", tone: "ok" },
  { label: "Forte", tone: "ok" },
];

export default function Register() {
  const { register } = useAuth();
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "", terms: false });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  const set = (key) => (e) =>
    setForm((f) => ({ ...f, [key]: e.target.type === "checkbox" ? e.target.checked : e.target.value }));

  const strength = passwordStrength(form.password);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError("");
    const next = {};
    if (form.name.trim().length < 2) next.name = "Informe seu nome.";
    if (!EMAIL_RE.test(form.email.trim())) next.email = "Informe um e-mail válido.";
    if (form.password.length < 8) next.password = "A senha deve ter ao menos 8 caracteres.";
    if (form.confirm !== form.password) next.confirm = "As senhas não coincidem.";
    if (!form.terms) next.terms = "É necessário aceitar os termos.";
    setErrors(next);

    if (Object.keys(next).length > 0) return;

    setLoading(true);
    try {
      await register(form.name, form.email, form.password);
      window.location.hash = ""; // Redireciona para a home autenticado
    } catch (err) {
      const msg = err.response?.data?.detail || "Erro ao criar conta. Tente novamente.";
      setApiError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Crie sua conta"
      subtitle="Comece a auditar publicações com IA em poucos minutos."
      footer={<>Já tem conta? <a href="#/login">Entrar</a></>}
    >
      <form className="auth-form" onSubmit={handleSubmit} noValidate>
        {apiError && (
          <div className="card error-card" style={{ marginTop: 0, padding: "12px 16px" }}>
            <span>⚠️</span>
            <p style={{ margin: 0 }}>{apiError}</p>
          </div>
        )}

        <Field label="Nome completo" placeholder="Seu nome" autoComplete="name"
          value={form.name} onChange={set("name")} error={errors.name} disabled={loading} />
        <Field label="E-mail" type="email" placeholder="voce@empresa.com" autoComplete="email"
          value={form.email} onChange={set("email")} error={errors.email} disabled={loading} />
        <Field label="Senha" type="password" placeholder="Mínimo de 8 caracteres" autoComplete="new-password"
          value={form.password} onChange={set("password")} error={errors.password} disabled={loading} />

        {form.password && (
          <div className="strength">
            <div className="meter">
              <span className={`tone-${STRENGTH[strength].tone}`} style={{ width: `${(strength / 4) * 100}%` }} />
            </div>
            <small className={`tone-${STRENGTH[strength].tone}`}>Senha: {STRENGTH[strength].label}</small>
          </div>
        )}

        <Field label="Confirmar senha" type="password" placeholder="Repita a senha" autoComplete="new-password"
          value={form.confirm} onChange={set("confirm")} error={errors.confirm} disabled={loading} />

        <label className="check">
          <input type="checkbox" checked={form.terms} onChange={set("terms")} disabled={loading} />
          <span>Concordo com os termos de uso e a política de privacidade</span>
        </label>
        {errors.terms && <span className="field-error">{errors.terms}</span>}

        <button type="submit" className="button auth-submit" disabled={loading}>
          {loading ? "Criando conta..." : "Criar conta"}
        </button>
      </form>
    </AuthLayout>
  );
}
