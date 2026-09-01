import React, { useState, useEffect, useRef } from 'react'
import './App.css'
import ChatContainer from './components/ChatContainer'
import { chatAPI, API_BASE_URL } from './api'

function App() {
  const [conversations, setConversations] = useState([])
  const [activeConversation, setActiveConversation] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [backendStatus, setBackendStatus] = useState('checking')
  const [attachment, setAttachment] = useState(null)
  const [lastFailedRequest, setLastFailedRequest] = useState(null)

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth()
  }, [])

  const checkBackendHealth = async () => {
    try {
      const health = await chatAPI.health()
      setBackendStatus(health.services?.agent === 'not_configured' ? 'degraded' : health.status)
    } catch (err) {
      console.error('Backend health check failed:', err)
      setBackendStatus('offline')
    }
  }

  const startNewChat = () => {
    // The server owns conversation IDs.  Keeping this state unset causes the
    // first submitted message to create a real conversation in one request.
    setConversations([])
    setActiveConversation(null)
    setMessages([])
    setError(null)
    setAttachment(null)
  }

  const handleSendMessage = async (message, retryAttachment = attachment) => {
    if (!message.trim()) {
      setError('Message cannot be empty')
      return
    }

    setError(null)
    setLastFailedRequest(null)
    setLoading(true)

    // Add user message immediately
    setMessages(prev => [...prev, {
      role: 'user',
      content: message,
      image: retryAttachment
    }])

    try {
      const response = await chatAPI.chat(message, activeConversation, retryAttachment?.file)

      if (!activeConversation) {
        setActiveConversation(response.conversation_id)
        setConversations([{ id: response.conversation_id, created: new Date() }])
      }

      // Add assistant response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.message
      }])

      setAttachment(null)
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to get response. Please try again.'
      setError(errorMessage)
      setLastFailedRequest({ message, attachment: retryAttachment })
      setMessages(prev => prev.slice(0, -1)) // Remove the failed pending user message
    } finally {
      setLoading(false)
    }
  }

  const retryLastRequest = () => {
    if (lastFailedRequest && !loading) {
      handleSendMessage(lastFailedRequest.message, lastFailedRequest.attachment)
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
          onDismissError={() => setError(null)}
          onRetry={lastFailedRequest ? retryLastRequest : null}
          isEmpty={messages.length === 0}
        />
      </div>
    </div>
  )
}

export default App
