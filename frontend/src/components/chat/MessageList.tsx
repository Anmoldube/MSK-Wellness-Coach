import { ChatMessage } from '../../types/chat.types';
import MessageBubble from './MessageBubble';

interface MessageListProps {
    messages: ChatMessage[];
}

function MessageList({ messages }: MessageListProps) {
    if (messages.length === 0) {
        return (
            <div className="empty-state">
                <div className="empty-icon">💬</div>
                <p>Start a conversation!</p>
            </div>
        );
    }

    return (
        <>
            {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
            ))}
        </>
    );
}

export default MessageList;
