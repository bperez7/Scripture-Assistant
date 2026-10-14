const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options)
  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail || `Request failed with status ${response.status}`)
  }
  return response.json()
}

export const getVolumes = () => request('/scriptures/volumes')
export const getBooks = volume => request(`/scriptures/books?volume=${encodeURIComponent(volume)}`)
export const getChapters = book => request(`/scriptures/books/${encodeURIComponent(book)}/chapters`)
export const getChapter = (book, chapter) => request(`/scriptures/books/${encodeURIComponent(book)}/chapters/${chapter}`)
export const searchScriptures = query => request(`/scriptures/search?q=${encodeURIComponent(query)}`)
export const askQuestion = question => request('/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question }) })
