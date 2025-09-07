const API_URL = import.meta.env.VITE_API_URL;

async function getHealth() {
  const res = await fetch(`${API_URL}/health`);
  const data = await res.json();
  console.log(data);
}
