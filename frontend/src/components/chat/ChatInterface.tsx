import { useChat } from '../../hooks/useChat';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import SuggestedQuestions from './SuggestedQuestions';
import './ChatInterface.css';

interface ChatInterfaceProps {
    userId: string;
}

function ChatInterface({ userId }: ChatInterfaceProps) {
    const {
        messages,
        isLoading,
        suggestedQuestions,
        sendMessage,
        messagesEndRef,
    } = useChat(userId);

    return (
        <div className="chat-interface">
            {/* Messages Area */}
            <div className="chat-messages-container">
                <div className="chat-messages">
                    <MessageList messages={messages} />
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <div className="chat-input-container">
                {/* Suggested Questions */}
                {suggestedQuestions.length > 0 && !isLoading && (
                    <SuggestedQuestions
                        questions={suggestedQuestions}
                        onSelect={sendMessage}
                    />
                )}

                {/* Message Input */}
                <MessageInput
                    onSend={sendMessage}
                    disabled={isLoading}
                    isLoading={isLoading}
                />
            </div>
        </div>
    );
}

export default ChatInterface;
