import React, { useEffect } from "react";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { AuthProvider } from "./context/AuthContext";
import { useHashRoute } from "./hooks/useHashRoute";
import { wakeUpBackend } from "./services/api";

function AppContent() {
  const route = useHashRoute();

  useEffect(() => {
    wakeUpBackend();
  }, []);

  if (route === "/login") return <Login />;
  if (route === "/cadastro") return <Register />;
  return <Landing />;
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
