document.getElementById("send").onclick = async () => {
  const token = document.getElementById("token").value.trim();
  const prompt = document.getElementById("prompt").value.trim();
  const out = document.getElementById("out");
  if (!token || !prompt) { out.textContent = "缺少 token 或 prompt"; return; }
  const url = (window.SERVICE_URL || "https://your-render-url.onrender.com") + "/chat";
  const resp = await fetch(url, {
    method: "POST",
    headers: {"Content-Type":"application/json","X-Access-Token":token},
    body: JSON.stringify({prompt})
  });
  out.textContent = await resp.text();
};