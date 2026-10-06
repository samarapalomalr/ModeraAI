import { useEffect } from "react";

import Home from "./pages/Home";
import "./styles/global.css";

import { wakeUpBackend } from "./services/api";

export default function App() {
  // Wakes up the backend when the app opens.
  useEffect(() => {
    wakeUpBackend();
  }, []);

  return <Home />;
}