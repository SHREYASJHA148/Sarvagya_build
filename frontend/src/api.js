import axios from 'axios'

const LOCAL_API_BASE = 'http://localhost:8000'
const PROD_API_BASE = 'https://sarvagya-buildbackend1-git-main-adu8.vercel.app'

const fallbackBase = import.meta.env.DEV ? '' : PROD_API_BASE
export const API_BASE_URL = (
  (import.meta.env.VITE_API_BASE_URL && import.meta.env.VITE_API_BASE_URL.trim()) ||
  fallbackBase
).replace(/\/+$/, '')

export const API_BASE = API_BASE_URL ? `${API_BASE_URL}/api` : '/api'

export const chatAPI = {
  async chat(message, conversationId, file) {
    const formData = new FormData()
    formData.append('message', message)
    if (conversationId) {
      formData.append('conversation_id', conversationId)
    }
    if (file) {
      formData.append('file', file)
    }

    const response = await axios.post(`${API_BASE}/chat`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  },

  async health() {
    const response = await axios.get(`${API_BASE}/health`)
    return response.data
  },

  async getConversation(conversationId) {
    const response = await axios.get(`${API_BASE}/conversations/${conversationId}`)
    return response.data
  },
}
