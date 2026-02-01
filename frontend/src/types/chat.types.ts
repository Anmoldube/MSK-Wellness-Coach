/**
 * TypeScript types for chat functionality
 */

export interface ChatMessage {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    isLoading?: boolean;
    suggestedQuestions?: string[];
}

export interface ChatRequest {
    message: string;
    conversation_id?: string;
    include_context?: boolean;
}

export interface ChatResponse {
    message: string;
    conversation_id: string;
    function_calls?: FunctionCall[];
    citations?: string[];
    suggested_questions?: string[];
}

export interface FunctionCall {
    name: string;
    arguments: Record<string, unknown>;
    result?: Record<string, unknown>;
}

export interface ConversationSummary {
    conversation_id: string;
    started_at: string;
    message_count: number;
    last_message_preview?: string;
}
