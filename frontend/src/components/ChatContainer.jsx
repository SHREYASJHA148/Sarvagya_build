import React, { useEffect, useRef } from 'react'
import './ChatContainer.css'

function ChatContainer({
  messages,
  loading,
  error,
  onSendMessage,
  onNewChat,
  attachment,
  onAttachmentChange,
  onRemoveAttachment,
  isEmpty
}) {
  const chatContainerRef = useRef(null)

  // Scroll to bottom on new messages
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [messages, loading])

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-title">
          <span className="chat-title-text">Sarvagya</span>
          <span className="chat-title-tag">AI Trading Chart Analysis</span>
        </div>
        <button
          className="btn-new-chat"
          onClick={onNewChat}
          disabled={loading}
        >
          New Chat
        </button>
      </div>

      {error && (
        <div className="error-banner">
          <span className="error-text">{error}</span>
          <button
            className="btn-error-close"
            onClick={() => {}}
          >
            ×
          </button>
        </div>
      )}

      <div ref={chatContainerRef} className="messages-container">
        {isEmpty ? (
          <EmptyState />
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">
                {msg.image && (
                  <div className="message-image">
                    <img src={msg.image.preview} alt="Chart preview" />
                  </div>
                )}
                <div className="message-text">
                  <div className="message-meta">
                    <span className="message-role">{msg.role === 'user' ? 'You' : 'Sarvagya'}</span>
                  </div>
                  <div className="message-body">
                    <pre>{msg.content}</pre>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}

        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="message-text">
                <div className="message-meta">
                  <span className="message-role">Sarvagya</span>
                </div>
                <div className="message-body">
                  <div className="loading-indicator">
                    <div className="loading-dot"></div>
                    <div className="loading-dot"></div>
                    <div className="loading-dot"></div>
                  </div>
                  <div className="loading-text">Analyzing your chart...</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <ChatComposer
        onSendMessage={onSendMessage}
        loading={loading}
        attachment={attachment}
        onAttachmentChange={onAttachmentChange}
        onRemoveAttachment={onRemoveAttachment}
        error={error}
      />
    </div>
  )
}

function EmptyState() {
  return (
    <div className="empty-state">
      <div className="empty-state-content">
        <div className="empty-state-icon">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>
            <path d="M16 8l-4 4-4-4"/>
          </svg>
        </div>
        <h2 className="empty-state-title">AI-Powered Chart Intelligence</h2>
        <p className="empty-state-description">
          Upload a trading chart image and ask questions about patterns, trends, and market structure.
        </p>
        <div className="empty-state-examples">
          <p>Try asking:</p>
          <ul className="example-prompts">
            <li>"Analyze this chart and explain the market structure"</li>
            <li>"What pattern do you see in this chart?"</li>
            <li>"Identify important levels visible on this chart"</li>
            <li>"Explain the bullish and bearish scenarios"</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

function ChatComposer({
  onSendMessage,
  loading,
  attachment,
  onAttachmentChange,
  onRemoveAttachment,
  error
}) {
  const [message, setMessage] = React.useState('')
  const fileInputRef = React.useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!loading && message.trim()) {
      onSendMessage(message)
      setMessage('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSubmit(e)
    }
  }

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      onAttachmentChange(file)
    }
  }

  return (
    <form className="chat-composer" onSubmit={handleSubmit}>
      {attachment && (
        <div className="attachment-preview">
          <div className="attachment-info">
            <span className="attachment-name">{attachment.name}</span>
            <button
              type="button"
              className="btn-remove-attachment"
              onClick={onRemoveAttachment}
            >
              ×
            </button>
          </div>
          <div className="attachment-image">
            <img src={attachment.preview} alt="Chart preview" />
          </div>
        </div>
      )}

      <div className="composer-controls">
        <button
          type="button"
          className="btn-attach"
          onClick={() => fileInputRef.current?.click()}
          disabled={loading}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"/>
          </svg>
          <input
            ref={fileInputRef}
            type="file"
            accept=".png,.jpg,.jpeg,.webp"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
        </button>

        <div className="composer-input-wrapper">
          <textarea
            className="composer-input"
            placeholder="Upload a chart and ask about patterns, trends, or market structure..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            rows="1"
            disabled={loading}
          />
          <div className="composer-hint">
            <span className="composer-hint-text">
              Enter for new line, Ctrl+Enter to send
            </span>
          </div>
        </div>

        <button
          type="submit"
          className="btn-send"
          disabled={loading || !message.trim()}
        >
          {loading ? (
            <svg className="loading-spinner" width="20" height="20" viewBox="0 0 24 24" stroke="currentColor">
              <path d="M12 2a10 10 0 0110 10" strokeWidth="2" fill="none"/>
            </svg>
          ) : (
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
          )}
        </button>
      </div>

      <div className="composer-footer">
        <p className="disclaimer">
          AI-generated analysis is for informational and educational purposes and is not guaranteed financial advice.
        </p>
      </div>
    </form>
  )
}

export default ChatContainer
