import { useState, FormEvent, KeyboardEvent } from 'react';
import './MessageInput.css';

interface MessageInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
    isLoading?: boolean;
}

function MessageInput({ onSend, disabled, isLoading }: MessageInputProps) {
    const [input, setInput] = useState('');

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (input.trim() && !disabled) {
            onSend(input);
            setInput('');
        }
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e as unknown as FormEvent);
        }
    };

    return (
        <form className="message-input-form" onSubmit={handleSubmit}>
            <div className="input-wrapper">
                <textarea
                    className="message-textarea"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask about your MSK wellness..."
                    disabled={disabled}
                    rows={1}
                    aria-label="Message input"
                />

                <button
                    type="submit"
                    className="send-button"
                    disabled={disabled || !input.trim()}
                    aria-label="Send message"
                >
                    {isLoading ? (
                        <div className="loading-spinner" />
                    ) : (
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                        </svg>
                    )}
                </button>
            </div>

            <p className="input-hint">
                Press Enter to send, Shift + Enter for new line
            </p>
        </form>
    );
}

export default MessageInput;
