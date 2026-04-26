import { useState, useRef, useCallback, useEffect } from 'react';
import { apiService } from '../services/api.service';
import { ChatMessage, ConversationSummary } from '../types/chat.types';

// Generate unique ID
const generateId = () => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

export function useChat(userId: string) {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [suggestedQuestions, setSuggestedQuestions] = useState<string[]>([]);
    const [conversations, setConversations] = useState<ConversationSummary[]>([]);
    const [conversationsLoading, setConversationsLoading] = useState(false);

    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Load conversations list
    const loadConversations = useCallback(async () => {
        if (!userId) return;
        setConversationsLoading(true);
        try {
            const convos = await apiService.getConversations(userId, 30);
            setConversations(convos);
        } catch (err) {
            console.error('Failed to load conversations:', err);
        } finally {
            setConversationsLoading(false);
        }
    }, [userId]);

    // Load on mount and userId change
    useEffect(() => {
        loadConversations();
    }, [loadConversations]);

    // Show welcome message
    const showWelcome = useCallback(() => {
        const welcomeMessage: ChatMessage = {
            id: generateId(),
            role: 'assistant',
            content: `Hello! 👋 I'm your **MSK Wellness Coach**. I'm here to help you understand your musculoskeletal health and improve it.

**I can help you with:**
- 📊 Understanding your assessment results
- 💪 Personalized exercise recommendations
- 📋 Care program suggestions
- 📄 Answering questions about your uploaded documents

What would you like to explore today?`,
            timestamp: new Date(),
            suggestedQuestions: [
                "What does my report say?",
                "How can I improve my balance?",
                "Which care program should I follow?"
            ]
        };
        setMessages([welcomeMessage]);
        setSuggestedQuestions(welcomeMessage.suggestedQuestions || []);
    }, []);

    // Initial greeting
    useEffect(() => {
        showWelcome();
    }, [showWelcome]);

    // Auto-scroll to bottom
    const scrollToBottom = useCallback(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages, scrollToBottom]);

    // Start a new conversation
    const startNewChat = useCallback(() => {
        setConversationId(null);
        setError(null);
        setSuggestedQuestions([]);
        showWelcome();
    }, [showWelcome]);

    // Load a previous conversation
    const loadConversation = useCallback(async (convId: string) => {
        setIsLoading(true);
        setError(null);
        try {
            const detail = await apiService.getConversation(convId);
            setConversationId(detail.conversation_id);

            const loadedMessages: ChatMessage[] = detail.messages.map((m, i) => ({
                id: `loaded_${i}_${Date.now()}`,
                role: m.role as 'user' | 'assistant',
                content: m.content,
                timestamp: new Date(m.timestamp),
            }));
            setMessages(loadedMessages);
            setSuggestedQuestions([]);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load conversation');
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Delete a conversation
    const deleteConversation = useCallback(async (convId: string) => {
        try {
            await apiService.deleteConversation(convId);
            setConversations(prev => prev.filter(c => c.conversation_id !== convId));
            if (convId === conversationId) {
                startNewChat();
            }
        } catch (err) {
            console.error('Failed to delete conversation:', err);
        }
    }, [conversationId, startNewChat]);

    // Send message
    const sendMessage = useCallback(async (content: string) => {
        if (!content.trim() || isLoading) return;

        setError(null);
        setIsLoading(true);
        setSuggestedQuestions([]);

        // Add user message
        const userMessage: ChatMessage = {
            id: generateId(),
            role: 'user',
            content: content.trim(),
            timestamp: new Date(),
        };
        setMessages(prev => [...prev, userMessage]);

        // Add loading message
        const loadingId = generateId();
        const loadingMessage: ChatMessage = {
            id: loadingId,
            role: 'assistant',
            content: '',
            timestamp: new Date(),
            isLoading: true,
        };
        setMessages(prev => [...prev, loadingMessage]);

        try {
            const response = await apiService.sendMessage({
                message: content.trim(),
                conversation_id: conversationId || undefined,
                include_context: true,
                user_id: userId,
            });

            // Update conversation ID
            if (response.conversation_id) {
                setConversationId(response.conversation_id);
            }

            // Replace loading message with actual response
            const assistantMessage: ChatMessage = {
                id: loadingId,
                role: 'assistant',
                content: response.message,
                timestamp: new Date(),
                suggestedQuestions: response.suggested_questions,
            };

            setMessages(prev =>
                prev.map(msg => msg.id === loadingId ? assistantMessage : msg)
            );

            // Update suggested questions
            if (response.suggested_questions?.length) {
                setSuggestedQuestions(response.suggested_questions);
            }

            // Refresh conversations list
            loadConversations();

        } catch (err) {
            // Remove loading message on error
            setMessages(prev => prev.filter(msg => msg.id !== loadingId));

            const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
            setError(errorMessage);

            // Add error message from assistant
            const errorResponse: ChatMessage = {
                id: generateId(),
                role: 'assistant',
                content: `I apologize, but I encountered an error: ${errorMessage}. Please try again.`,
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, errorResponse]);
        } finally {
            setIsLoading(false);
        }
    }, [conversationId, isLoading, userId, loadConversations]);

    // Clear conversation
    const clearConversation = useCallback(() => {
        setMessages([]);
        setConversationId(null);
        setSuggestedQuestions([]);
        setError(null);
    }, []);

    return {
        messages,
        isLoading,
        error,
        suggestedQuestions,
        conversations,
        conversationsLoading,
        conversationId,
        sendMessage,
        clearConversation,
        startNewChat,
        loadConversation,
        deleteConversation,
        loadConversations,
        messagesEndRef,
    };
}
