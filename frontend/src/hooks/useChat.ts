import { useState, useRef, useCallback, useEffect } from 'react';
import { apiService } from '../services/api.service';
import { ChatMessage } from '../types/chat.types';

// Generate unique ID
const generateId = () => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

export function useChat(userId: string) {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [suggestedQuestions, setSuggestedQuestions] = useState<string[]>([]);

    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Initial greeting
    useEffect(() => {
        const welcomeMessage: ChatMessage = {
            id: generateId(),
            role: 'assistant',
            content: `Hello! 👋 I'm your **MSK Wellness Coach**. I'm here to help you understand your musculoskeletal health and improve it.

**I can help you with:**
- 📊 Understanding your assessment results
- 💪 Personalized exercise recommendations
- 📋 Care program suggestions
- 🛒 Product recommendations

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

    // Auto-scroll to bottom
    const scrollToBottom = useCallback(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages, scrollToBottom]);

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
    }, [conversationId, isLoading]);

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
        sendMessage,
        clearConversation,
        messagesEndRef,
    };
}
