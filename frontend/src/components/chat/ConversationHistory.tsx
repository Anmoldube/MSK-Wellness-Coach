import { useState } from 'react';
import { ConversationSummary } from '../../types/chat.types';
import './ConversationHistory.css';

interface ConversationHistoryProps {
    conversations: ConversationSummary[];
    activeId: string | null;
    loading: boolean;
    onSelect: (id: string) => void;
    onDelete: (id: string) => void;
    onNewChat: () => void;
}

function ConversationHistory({
    conversations,
    activeId,
    loading,
    onSelect,
    onDelete,
    onNewChat,
}: ConversationHistoryProps) {
    const [search, setSearch] = useState('');

    const filtered = conversations.filter(c => {
        if (!search) return true;
        const q = search.toLowerCase();
        return (
            (c.title || '').toLowerCase().includes(q) ||
            (c.last_message_preview || '').toLowerCase().includes(q)
        );
    });

    // Group by relative date
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today.getTime() - 86400000);
    const lastWeek = new Date(today.getTime() - 7 * 86400000);

    const groups: { label: string; items: ConversationSummary[] }[] = [
        { label: 'Today', items: [] },
        { label: 'Yesterday', items: [] },
        { label: 'Last 7 Days', items: [] },
        { label: 'Older', items: [] },
    ];

    filtered.forEach(c => {
        const d = new Date(c.started_at);
        if (d >= today) groups[0].items.push(c);
        else if (d >= yesterday) groups[1].items.push(c);
        else if (d >= lastWeek) groups[2].items.push(c);
        else groups[3].items.push(c);
    });

    return (
        <div className="conv-history">
            {/* New Chat Button */}
            <button className="conv-new-btn" onClick={onNewChat}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="12" y1="5" x2="12" y2="19" />
                    <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
                New Chat
            </button>

            {/* Search */}
            <div className="conv-search">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
                <input
                    type="text"
                    placeholder="Search conversations…"
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                />
            </div>

            {/* Conversation List */}
            <div className="conv-list">
                {loading && <div className="conv-loading">Loading…</div>}

                {!loading && filtered.length === 0 && (
                    <div className="conv-empty">No conversations yet</div>
                )}

                {groups.map(group =>
                    group.items.length > 0 ? (
                        <div key={group.label} className="conv-group">
                            <div className="conv-group-label">{group.label}</div>
                            {group.items.map(c => (
                                <div
                                    key={c.conversation_id}
                                    className={`conv-item ${c.conversation_id === activeId ? 'active' : ''}`}
                                    onClick={() => onSelect(c.conversation_id)}
                                >
                                    <div className="conv-item-icon">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
                                        </svg>
                                    </div>
                                    <div className="conv-item-info">
                                        <span className="conv-item-title">
                                            {c.title || c.last_message_preview || 'Untitled'}
                                        </span>
                                        <span className="conv-item-meta">
                                            {c.message_count} messages
                                        </span>
                                    </div>
                                    <button
                                        className="conv-item-delete"
                                        onClick={e => {
                                            e.stopPropagation();
                                            onDelete(c.conversation_id);
                                        }}
                                        title="Delete"
                                    >
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <polyline points="3 6 5 6 21 6" />
                                            <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                                        </svg>
                                    </button>
                                </div>
                            ))}
                        </div>
                    ) : null
                )}
            </div>
        </div>
    );
}

export default ConversationHistory;
