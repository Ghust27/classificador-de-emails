const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/+$/, "")

export async function classifyEmailFromFile(file) {
  const formData = new FormData()
  formData.append("file", file)

  const response = await fetch(`${API_URL}/api/classify`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    const error = {
      message: `Erro ao classificar email: ${response.statusText}`,
      status: response.status,
    }
    throw error
  }

  const data = await response.json()
  return data
}

export async function classifyEmailFromText(text) {
  const response = await fetch(`${API_URL}/api/classify`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  })

  if (!response.ok) {
    const error = {
      message: `Erro ao classificar email: ${response.statusText}`,
      status: response.status,
    }
    throw error
  }

  const data = await response.json()
  return data
}
