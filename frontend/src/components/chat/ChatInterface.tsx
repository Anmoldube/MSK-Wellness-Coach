import { useState } from 'react';
import { useChat } from '../../hooks/useChat';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import SuggestedQuestions from './SuggestedQuestions';
import ConversationHistory from './ConversationHistory';
import DocumentUpload from './DocumentUpload';
import './ChatInterface.css';

interface ChatInterfaceProps {
    userId: string;
}

type SidebarTab = 'history' | 'documents';

function ChatInterface({ userId }: ChatInterfaceProps) {
    const {
        messages,
        isLoading,
        suggestedQuestions,
        conversations,
        conversationsLoading,
        conversationId,
        sendMessage,
        startNewChat,
        loadConversation,
        deleteConversation,
        messagesEndRef,
    } = useChat(userId);

    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [activeTab, setActiveTab] = useState<SidebarTab>('history');

    return (
        <div className="chat-layout">
            {/* Sidebar */}
            <aside className={`chat-sidebar ${sidebarOpen ? 'open' : 'collapsed'}`}>
                {/* Sidebar Toggle (inside sidebar) */}
                <button
                    className="sidebar-toggle"
                    onClick={() => setSidebarOpen(!sidebarOpen)}
                    title={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
                >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        {sidebarOpen ? (
                            <polyline points="15 18 9 12 15 6" />
                        ) : (
                            <polyline points="9 18 15 12 9 6" />
                        )}
                    </svg>
                </button>

                {sidebarOpen && (
                    <>
                        {/* Tab Switcher */}
                        <div className="sidebar-tabs">
                            <button
                                className={`sidebar-tab ${activeTab === 'history' ? 'active' : ''}`}
                                onClick={() => setActiveTab('history')}
                            >
                                💬 Chats
                            </button>
                            <button
                                className={`sidebar-tab ${activeTab === 'documents' ? 'active' : ''}`}
                                onClick={() => setActiveTab('documents')}
                            >
                                📄 Docs
                            </button>
                        </div>

                        {/* Tab Content */}
                        <div className="sidebar-content">
                            {activeTab === 'history' ? (
                                <ConversationHistory
                                    conversations={conversations}
                                    activeId={conversationId}
                                    loading={conversationsLoading}
                                    onSelect={loadConversation}
                                    onDelete={deleteConversation}
                                    onNewChat={startNewChat}
                                />
                            ) : (
                                <DocumentUpload userId={userId} />
                            )}
                        </div>
                    </>
                )}
            </aside>

            {/* Main Chat Area */}
            <div className="chat-main">
                <div className="chat-interface">
                    {/* Collapsed sidebar toggle (floating) */}
                    {!sidebarOpen && (
                        <button
                            className="sidebar-float-toggle"
                            onClick={() => setSidebarOpen(true)}
                            title="Open sidebar"
                        >
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <line x1="3" y1="6" x2="21" y2="6" />
                                <line x1="3" y1="12" x2="21" y2="12" />
                                <line x1="3" y1="18" x2="21" y2="18" />
                            </svg>
                        </button>
                    )}

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
            </div>
        </div>
    );
}

export default ChatInterface;
