import { Message } from '../App'
import './ChatMessage.css'

interface ChatMessageProps {
  message: Message;
}

function ChatMessage({ message }: ChatMessageProps) {
  const { text, sender, timestamp } = message

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className={`message ${sender}`}>
      <div className="message-content">
        <div className="message-avatar">
          {sender === 'user' ? '👤' : '🤖'}
        </div>
        <div className="message-bubble">
          <p className="message-text">{text}</p>
          <span className="message-time">{formatTime(timestamp)}</span>
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
