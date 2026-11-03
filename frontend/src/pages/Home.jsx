import React from "react";
import TextInput from "../components/TextInput";
import ResultCard from "../components/ResultCard";
import Loader from "../components/Loader";
import { useAnalyze } from "../hooks/useAnalyze";

export default function Home() {
  const { analyze, data, loading, error, reset } = useAnalyze();

  return (
    <div className="container">
      {/* HEADER */}
      <div style={{ marginBottom: 30, textAlign: "center" }}>
        <h1 className="title">ModeraAI</h1>
        <p className="subtitle" style={{ color: "#64748b", marginTop: 8 }}>
          Auditor e moderador inteligente para Instagram, TikTok e YouTube.
        </p>
      </div>

      {/* INPUT COM SELETOR */}
      <TextInput 
        key={data ? "analisado" : "novo"} 
        onSubmit={analyze} 
        loading={loading} 
      />

      {/* MENSAGEM DE ERRO AMIGÁVEL */}
      {error && (
        <div 
          className="card" 
          style={{ 
            marginTop: 20, 
            backgroundColor: "#fef2f2", 
            borderLeft: "4px solid #ef4444", 
            padding: "16px 20px" 
          }}
        >
          <div style={{ display: "flex", alignItems: "flex-start", gap: "12px" }}>
            <span style={{ fontSize: "20px" }}>⚠️</span>
            <div>
              <h4 style={{ margin: 0, color: "#991b1b", fontWeight: "600", fontSize: "15px" }}>
                Não foi possível concluir a análise
              </h4>
              <p style={{ margin: "4px 0 0 0", color: "#b91c1c", fontSize: "14px", lineHeight: "1.4" }}>
                {error}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* LOADING */}
      {loading && <Loader />}

      {/* RESULT */}
      {data && !loading && (
        <>
          <ResultCard data={data} />

          <div style={{ marginTop: 20, textAlign: "center" }}>
            <button className="button" onClick={reset}>
              Analisar novo post
            </button>
          </div>
        </>
      )}
    </div>
  );
}