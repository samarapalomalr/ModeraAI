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
      <div style={{ marginBottom: 40 }}>
        <h1 className="title">ModeraAI</h1>
        <p className="subtitle">
          
        </p>
      </div>

      {/* INPUT */}
      <TextInput 
        key={data ? "analisado" : "novo"} 
        onSubmit={analyze} 
        loading={loading} 
      />

      {/* ERROR */}
      {error && (
        <div className="card" style={{ marginTop: 20 }}>
          <p style={{ color: "#ef4444" }}>❌ {error}</p>
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