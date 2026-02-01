import './SuggestedQuestions.css';

interface SuggestedQuestionsProps {
    questions: string[];
    onSelect: (question: string) => void;
}

function SuggestedQuestions({ questions, onSelect }: SuggestedQuestionsProps) {
    if (!questions || questions.length === 0) return null;

    return (
        <div className="suggested-questions">
            <span className="suggested-label">Suggested:</span>
            <div className="questions-list">
                {questions.map((question, index) => (
                    <button
                        key={index}
                        className="question-chip"
                        onClick={() => onSelect(question)}
                        type="button"
                    >
                        {question}
                    </button>
                ))}
            </div>
        </div>
    );
}

export default SuggestedQuestions;
