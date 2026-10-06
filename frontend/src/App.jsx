import React, { useEffect } from "react"; 
import Home from "./pages/Home";
import { wakeUpBackend } from "./services/api";

export default function App() {
  useEffect(() => {
    wakeUpBackend();
  }, []);

  return <Home />;
}