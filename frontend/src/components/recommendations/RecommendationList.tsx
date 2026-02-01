import { useState, useEffect } from 'react';
import { apiService } from '../../services/api.service';
import './RecommendationList.css';

interface Exercise {
    exercise_id: string;
    name: string;
    category: string;
    difficulty: string;
    instructions: string[];
    sets_reps: string;
    frequency: string;
    safety_notes: string[];
}

interface CareProgram {
    program_id: string;
    name: string;
    provider: string;
    description: string;
    focus_areas: string[];
    duration_weeks: number;
    intensity: string;
    cost?: number;
}

interface Product {
    product_id: string;
    name: string;
    type: string;
    description: string;
    use_cases: string[];
    price?: number;
}

type RecommendationType = 'exercises' | 'programs' | 'products';

function RecommendationList() {
    const [activeTab, setActiveTab] = useState<RecommendationType>('exercises');
    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [programs, setPrograms] = useState<CareProgram[]>([]);
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(false);
    const [expandedItem, setExpandedItem] = useState<string | null>(null);

    useEffect(() => {
        loadData(activeTab);
    }, [activeTab]);

    const loadData = async (type: RecommendationType) => {
        setLoading(true);
        try {
            switch (type) {
                case 'exercises':
                    const exerciseData = await apiService.getExercises();
                    setExercises(exerciseData as Exercise[]);
                    break;
                case 'programs':
                    const programData = await apiService.getCarePrograms();
                    setPrograms(programData as CareProgram[]);
                    break;
                case 'products':
                    const productData = await apiService.getProducts();
                    setProducts(productData as Product[]);
                    break;
            }
        } catch (err) {
            console.error('Failed to load recommendations:', err);
        } finally {
            setLoading(false);
        }
    };

    const getDifficultyColor = (difficulty: string) => {
        switch (difficulty?.toLowerCase()) {
            case 'easy': return 'difficulty-easy';
            case 'moderate': return 'difficulty-moderate';
            case 'hard': return 'difficulty-hard';
            default: return '';
        }
    };

    return (
        <div className="recommendations">
            {/* Tabs */}
            <div className="rec-tabs">
                <button
                    className={`tab ${activeTab === 'exercises' ? 'active' : ''}`}
                    onClick={() => setActiveTab('exercises')}
                >
                    💪 Exercises
                </button>
                <button
                    className={`tab ${activeTab === 'programs' ? 'active' : ''}`}
                    onClick={() => setActiveTab('programs')}
                >
                    📋 Programs
                </button>
                <button
                    className={`tab ${activeTab === 'products' ? 'active' : ''}`}
                    onClick={() => setActiveTab('products')}
                >
                    🛒 Products
                </button>
            </div>

            {/* Content */}
            <div className="rec-content">
                {loading ? (
                    <div className="rec-loading">
                        <div className="loading-spinner-lg"></div>
                    </div>
                ) : (
                    <>
                        {/* Exercises */}
                        {activeTab === 'exercises' && (
                            <div className="rec-list">
                                {exercises.map((exercise) => (
                                    <div key={exercise.exercise_id} className="rec-card">
                                        <div
                                            className="rec-card-header"
                                            onClick={() => setExpandedItem(
                                                expandedItem === exercise.exercise_id ? null : exercise.exercise_id
                                            )}
                                        >
                                            <div className="rec-info">
                                                <h4>{exercise.name}</h4>
                                                <div className="rec-meta">
                                                    <span className="rec-category">{exercise.category}</span>
                                                    <span className={`rec-difficulty ${getDifficultyColor(exercise.difficulty)}`}>
                                                        {exercise.difficulty}
                                                    </span>
                                                </div>
                                            </div>
                                            <svg
                                                className={`expand-icon ${expandedItem === exercise.exercise_id ? 'expanded' : ''}`}
                                                width="20"
                                                height="20"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                strokeWidth="2"
                                            >
                                                <polyline points="6 9 12 15 18 9" />
                                            </svg>
                                        </div>

                                        {expandedItem === exercise.exercise_id && (
                                            <div className="rec-card-body">
                                                <div className="exercise-details">
                                                    <div className="detail-section">
                                                        <h5>Instructions</h5>
                                                        <ol>
                                                            {exercise.instructions.map((step, i) => (
                                                                <li key={i}>{step}</li>
                                                            ))}
                                                        </ol>
                                                    </div>
                                                    <div className="detail-row">
                                                        <span><strong>Sets/Reps:</strong> {exercise.sets_reps}</span>
                                                        <span><strong>Frequency:</strong> {exercise.frequency}</span>
                                                    </div>
                                                    {exercise.safety_notes.length > 0 && (
                                                        <div className="safety-notes">
                                                            <h5>⚠️ Safety Notes</h5>
                                                            <ul>
                                                                {exercise.safety_notes.map((note, i) => (
                                                                    <li key={i}>{note}</li>
                                                                ))}
                                                            </ul>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Programs */}
                        {activeTab === 'programs' && (
                            <div className="rec-list">
                                {programs.map((program) => (
                                    <div key={program.program_id} className="rec-card program-card">
                                        <div className="rec-card-header">
                                            <div className="rec-info">
                                                <h4>{program.name}</h4>
                                                <span className="provider">{program.provider}</span>
                                            </div>
                                            {program.cost && (
                                                <span className="price">${program.cost}</span>
                                            )}
                                        </div>
                                        <div className="rec-card-body">
                                            <p className="description">{program.description}</p>
                                            <div className="program-meta">
                                                <span>📅 {program.duration_weeks} weeks</span>
                                                <span>⚡ {program.intensity}</span>
                                            </div>
                                            <div className="focus-areas">
                                                {program.focus_areas.map((area) => (
                                                    <span key={area} className="focus-tag">{area}</span>
                                                ))}
                                            </div>
                                            <button className="enroll-btn">Learn More</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Products */}
                        {activeTab === 'products' && (
                            <div className="rec-list products-grid">
                                {products.map((product) => (
                                    <div key={product.product_id} className="rec-card product-card">
                                        <div className="product-type">{product.type}</div>
                                        <h4>{product.name}</h4>
                                        <p className="description">{product.description}</p>
                                        {product.price && (
                                            <span className="price">${product.price}</span>
                                        )}
                                        <div className="use-cases">
                                            {product.use_cases.slice(0, 3).map((useCase) => (
                                                <span key={useCase} className="use-tag">{useCase.replace(/_/g, ' ')}</span>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}

export default RecommendationList;
