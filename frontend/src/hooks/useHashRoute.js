import { useEffect, useState } from "react";

// Roteamento simples por hash (#/login, #/cadastro). Sem dependências extras.
// Âncoras da landing (#demo, #recursos...) não são rotas e caem em "/".
const ROUTES = ["/login", "/cadastro"];

function readRoute() {
  const hash = window.location.hash.replace(/^#/, "");
  return ROUTES.includes(hash) ? hash : "/";
}

export function useHashRoute() {
  const [route, setRoute] = useState(readRoute);

  useEffect(() => {
    const onChange = () => {
      const next = readRoute();
      setRoute((prev) => {
        if (prev !== next) window.scrollTo(0, 0);
        return next;
      });
    };
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);

  return route;
}
