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
    user_id?: string;
}

export interface ChatResponse {
    message: string;
    conversation_id: string;
    function_calls?: FunctionCall[];
    citations?: string[];
    suggested_questions?: string[];
    rag_sources?: RagSource[];
}

export interface FunctionCall {
    name: string;
    arguments: Record<string, unknown>;
    result?: Record<string, unknown>;
}

export interface RagSource {
    filename: string;
    page: number;
    doc_id: string;
}

export interface ConversationSummary {
    conversation_id: string;
    title?: string;
    started_at: string;
    message_count: number;
    last_message_preview?: string;
}

export interface ConversationDetail {
    conversation_id: string;
    user_id: string;
    messages: Array<{
        role: 'user' | 'assistant';
        content: string;
        timestamp: string;
    }>;
    started_at: string;
}

export interface UserDocument {
    doc_id: string;
    filename: string;
    file_type: string;
    page_count: number;
    chunk_count: number;
    status: 'processing' | 'indexed' | 'failed';
    created_at: string;
}
