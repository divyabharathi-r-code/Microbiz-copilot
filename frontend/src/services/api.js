const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options) {
  const response = await fetch(`${API}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail || 'Something went wrong')
  return response.json()
}
export const api = {
  summary: () => request('/api/dashboard/summary'),
  orders: () => request('/api/orders'),
  eligible: () => request('/api/reminders/eligible'),
  chat: message => request('/api/copilot/chat', { method: 'POST', body: JSON.stringify({ message }) }),
  draft: order_id => request('/api/reminders/draft', { method: 'POST', body: JSON.stringify({ order_id }) }),
}
