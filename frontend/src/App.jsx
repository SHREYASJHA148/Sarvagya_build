import React, { useState, useEffect, useRef } from 'react'
import './App.css'
import ChatContainer from './components/ChatContainer'
import { chatAPI } from './api'

function App() {
  const [conversations, setConversations] = useState([])
  const [activeConversation, setActiveConversation] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [backendStatus, setBackendStatus] = useState('checking')
  const [attachment, setAttachment] = useState(null)

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth()
  }, [])

  const checkBackendHealth = async () => {
    try {
      const health = await chatAPI.health()
      setBackendStatus(health.status)
    } catch (err) {
      console.error('Backend health check failed:', err)
      setBackendStatus('offline')
    }
  }

  const startNewChat = () => {
    const conversationId = `conv_${Date.now()}`
    setConversations(prev => [...prev, { id: conversationId, created: new Date() }])
    setActiveConversation(conversationId)
    setMessages([])
    setError(null)
    setAttachment(null)
  }

  const handleSendMessage = async (message) => {
    if (!message.trim()) {
      setError('Message cannot be empty')
      return
    }

    if (!activeConversation) {
      startNewChat()
      return
    }

    setError(null)
    setLoading(true)

    // Add user message immediately
    setMessages(prev => [...prev, {
      role: 'user',
      content: message,
      image: attachment
    }])

    try {
      const response = await chatAPI.chat(message, activeConversation, attachment?.file)

      // Add assistant response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.message
      }])

      setAttachment(null)
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to get response. Please try again.'
      setError(errorMessage)
      setMessages(prev => prev.filter((_, i) => i !== prev.length - 1)) // Remove pending user message
    } finally {
      setLoading(false)
    }
  }

  const handleAttachmentChange = (file) => {
    if (!file) {
      setAttachment(null)
      return
    }

    // Validate file
    const allowedTypes = ['image/png', 'image/jpeg', 'image/webp']
    const maxSize = 10 * 1024 * 1024

    if (!allowedTypes.includes(file.type)) {
      setError('Unsupported file type. Supported: PNG, JPG, WebP')
      return
    }

    if (file.size > maxSize) {
      setError('File size too large. Maximum: 10MB')
      return
    }

    setAttachment({
      file,
      name: file.name,
      preview: URL.createObjectURL(file)
    })
    setError(null)
  }

  const handleRemoveAttachment = () => {
    if (attachment?.preview) {
      URL.revokeObjectURL(attachment.preview)
    }
    setAttachment(null)
  }

  return (
    <div className="app">
      {backendStatus === 'offline' && (
        <div className="backend-banner error">
          ⚠️ Backend offline. Please ensure the API server is running on localhost:8000
        </div>
      )}
      {backendStatus === 'degraded' && (
        <div className="backend-banner warning">
          ⚠️ Google API key not configured. Chart analysis may not work.
        </div>
      )}

      <div className="app-layout">
        <ChatContainer
          messages={messages}
          loading={loading}
          error={error}
          onSendMessage={handleSendMessage}
          onNewChat={startNewChat}
          attachment={attachment}
          onAttachmentChange={handleAttachmentChange}
          onRemoveAttachment={handleRemoveAttachment}
          isEmpty={messages.length === 0}
        />
      </div>
    </div>
  )
}

export default App
