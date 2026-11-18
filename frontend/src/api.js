const API_BASE = "";

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  return res.json();
}

export async function fetchProgress() {
  const res = await fetch(`${API_BASE}/api/progress`);
  return res.json();
}

export async function convertToHinglish(projectId) {
  const res = await fetch(`${API_BASE}/api/convert-hinglish/${projectId}`, {
    method: "POST"
  });
  if (!res.ok) throw new Error("Hinglish conversion failed");
  return res.json();
}

export async function updateClipWords(payload) {
  const res = await fetch(`${API_BASE}/api/update-clip-words`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Failed to update words");
  return res.json();
}

export async function fetchPresets() {
  const res = await fetch(`${API_BASE}/api/presets`);
  return res.json();
}

export async function fetchProjects() {
  const res = await fetch(`${API_BASE}/api/projects`);
  return res.json();
}

export async function fetchProject(id) {
  const res = await fetch(`${API_BASE}/api/projects/${id}`);
  return res.json();
}

export async function uploadVideoFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("auto_generate", "true");
  const res = await fetch(`${API_BASE}/api/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function importYouTube(url) {
  const res = await fetch(`${API_BASE}/api/youtube`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, auto_generate: true }),
  });
  if (!res.ok) throw new Error("YouTube import failed");
  return res.json();
}

export async function importLiveStream(stream_url, duration_sec = 60) {
  const res = await fetch(`${API_BASE}/api/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ stream_url, duration_sec, auto_generate: true }),
  });
  if (!res.ok) throw new Error("Stream capture failed");
  return res.json();
}

export async function renderClip(payload) {
  const res = await fetch(`${API_BASE}/api/render-clip`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Clip rendering failed");
  return res.json();
}

export async function batchRender(payload) {
  const res = await fetch(`${API_BASE}/api/batch-render`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Batch render failed");
  return res.json();
}
