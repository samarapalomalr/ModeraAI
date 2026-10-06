export default function Loader() {
    return (
      <div className="card" style={{ textAlign: "center" }}>
        <p className="loader-highlight">
          Analisando dados ... 
        </p>
  
        <p className="loader">
          Isso pode levar alguns segundos
        </p>
  
        <div className="loader-dot"></div>
      </div>
    );
  }