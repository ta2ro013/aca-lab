import { useState } from "react";

const API = import.meta.env.VITE_API_URL;

function sessionId(): string {
  let id = localStorage.getItem("sid");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("sid", id);
  }
  return id;
}

export default function App() {
  const [log, setLog] = useState<string[]>([]);

  const hit = async () => {
    const res = await fetch(`${API}/api/counter`, {
      method: "POST",
      headers: { "X-Session-Id": sessionId() },
    });
    const { count, replica } = await res.json();
    setLog((l) => [`count=${count}  (${replica})`, ...l]);
  };

  return (
    <main>
      <h1>ACA Lab</h1>
      <button onClick={hit}>+1</button>
      <ul>
        {log.map((line, i) => (
          <li key={i}>{line}</li>
        ))}
      </ul>
    </main>
  );
}