import { useState } from "react";

export default function Field({ label, type = "text", error, ...props }) {
  const [show, setShow] = useState(false);
  const isPassword = type === "password";

  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <span className="field-wrap">
        <input
          className={`input ${error ? "invalid" : ""}`}
          type={isPassword && show ? "text" : type}
          aria-invalid={Boolean(error)}
          {...props}
        />
        {isPassword && (
          <button
            type="button"
            className="field-toggle"
            onClick={() => setShow((s) => !s)}
            aria-label={show ? "Ocultar senha" : "Mostrar senha"}
          >
            {show ? "🙈" : "👁️"}
          </button>
        )}
      </span>
      {error && <span className="field-error">{error}</span>}
    </label>
  );
}
