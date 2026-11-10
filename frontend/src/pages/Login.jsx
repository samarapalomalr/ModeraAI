import { useState } from "react";
import AuthLayout from "../components/AuthLayout";
import Field from "../components/Field";
import { useAuth } from "../context/AuthContext";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function Login() {
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "", remember: true });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  const set = (key) => (e) =>
    setForm((f) => ({ ...f, [key]: e.target.type === "checkbox" ? e.target.checked : e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError("");
    const next = {};
    if (!EMAIL_RE.test(form.email.trim())) next.email = "Informe um e-mail válido.";
    if (!form.password) next.password = "Informe sua senha.";
    setErrors(next);

    if (Object.keys(next).length > 0) return;

    setLoading(true);
    try {
      await login(form.email, form.password);
      window.location.hash = ""; // Redireciona para a home autenticado
    } catch (err) {
      const msg = err.response?.data?.detail || "E-mail ou senha incorretos.";
      setApiError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Bem-vindo de volta"
      subtitle="Entre na sua conta para continuar auditando conteúdos."
      footer={<>Ainda não tem conta? <a href="#/cadastro">Criar conta</a></>}
    >
      <form className="auth-form" onSubmit={handleSubmit} noValidate>
        {apiError && (
          <div className="card error-card" style={{ marginTop: 0, padding: "12px 16px" }}>
            <span>⚠️</span>
            <p style={{ margin: 0 }}>{apiError}</p>
          </div>
        )}

        <Field label="E-mail" type="email" placeholder="voce@empresa.com" autoComplete="email"
          value={form.email} onChange={set("email")} error={errors.email} disabled={loading} />
        <Field label="Senha" type="password" placeholder="Sua senha" autoComplete="current-password"
          value={form.password} onChange={set("password")} error={errors.password} disabled={loading} />

        <label className="check">
          <input type="checkbox" checked={form.remember} onChange={set("remember")} disabled={loading} />
          <span>Manter conectado</span>
        </label>

        <button type="submit" className="button auth-submit" disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </AuthLayout>
  );
}
