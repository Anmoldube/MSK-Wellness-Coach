import { ChatMessage } from '../../types/chat.types';
import ReactMarkdown from 'react-markdown';
import './MessageBubble.css';

interface MessageBubbleProps {
    message: ChatMessage;
}

function MessageBubble({ message }: MessageBubbleProps) {
    const isUser = message.role === 'user';
    const isLoading = message.isLoading;

    return (
        <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
            {/* Avatar */}
            <div className="message-avatar">
                {isUser ? (
                    <div className="avatar avatar-user">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 4a4 4 0 014 4 4 4 0 01-4 4 4 4 0 01-4-4 4 4 0 014-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4z" />
                        </svg>
                    </div>
                ) : (
                    <div className="avatar avatar-assistant">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                            <path
                                d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"
                                fill="url(#avatar-gradient)"
                            />
                            <defs>
                                <linearGradient id="avatar-gradient" x1="2" y1="2" x2="22" y2="21">
                                    <stop stopColor="#2ea3ff" />
                                    <stop offset="1" stopColor="#22c55e" />
                                </linearGradient>
                            </defs>
                        </svg>
                    </div>
                )}
            </div>

            {/* Content */}
            <div className="message-content">
                <div className={`message-bubble ${isUser ? 'bubble-user' : 'bubble-assistant'}`}>
                    {isLoading ? (
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    ) : (
                        <div className="message-text">
                            <ReactMarkdown
                                components={{
                                    p: ({ children }) => <p>{children}</p>,
                                    strong: ({ children }) => <strong>{children}</strong>,
                                    em: ({ children }) => <em>{children}</em>,
                                    ul: ({ children }) => <ul>{children}</ul>,
                                    ol: ({ children }) => <ol>{children}</ol>,
                                    li: ({ children }) => <li>{children}</li>,
                                    h1: ({ children }) => <h4>{children}</h4>,
                                    h2: ({ children }) => <h4>{children}</h4>,
                                    h3: ({ children }) => <h4>{children}</h4>,
                                    code: ({ children }) => <code>{children}</code>,
                                }}
                            >
                                {message.content}
                            </ReactMarkdown>
                        </div>
                    )}
                </div>

                {/* Timestamp */}
                <div className="message-meta">
                    <span className="message-time">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                </div>
            </div>
        </div>
    );
}

export default MessageBubble;
