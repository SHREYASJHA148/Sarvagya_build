import axios from 'axios'

const API_BASE = '/api'

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
