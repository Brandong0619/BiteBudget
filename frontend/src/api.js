const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function fetchGoals() {
  const res = await fetch(`${API_BASE}/api/goals`)
  if (!res.ok) throw new Error('Failed to load goals')
  return res.json()
}

export async function fetchRecommendations({ budget, goal, lat, lng }) {
  const res = await fetch(`${API_BASE}/api/recommendations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ budget, goal, lat, lng }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Failed to get recommendations')
  }
  return res.json()
}

export function getCurrentPosition() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation not supported'))
      return
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      (err) => reject(err),
      { enableHighAccuracy: true, timeout: 10000 },
    )
  })
}
