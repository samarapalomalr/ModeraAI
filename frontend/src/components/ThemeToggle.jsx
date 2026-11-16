export default function ThemeToggle({ theme, onToggle, inline = false }) {
  const next = theme === "dark" ? "claro" : "escuro";
  return (
    <button
      type="button"
      className={`theme-toggle ${inline ? "inline" : ""}`}
      onClick={onToggle}
      aria-label={`Mudar para tema ${next}`}
      title={`Mudar para tema ${next}`}
    >
      {theme === "dark" ? "☀️" : "🌙"}
    </button>
  );
}
