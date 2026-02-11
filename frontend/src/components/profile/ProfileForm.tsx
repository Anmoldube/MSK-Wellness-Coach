import { useState } from 'react';
import './ProfileForm.css';

interface PerformanceData {
    reaction_time?: number;
    accuracy?: number;
    score?: number;
    playtime_hours?: number;
    endurance?: number;
    strength?: number;
    flexibility?: number;
    balance?: number;
}

interface ProfileFormProps {
    onProfileCreated: (userId: string, userName: string) => void;
}

function ProfileForm({ onProfileCreated }: ProfileFormProps) {
    const [name, setName] = useState('');
    const [perfData, setPerfData] = useState<PerformanceData>({
        reaction_time: undefined,
        accuracy: undefined,
        score: undefined,
        playtime_hours: undefined,
        endurance: undefined,
        strength: undefined,
        flexibility: undefined,
        balance: undefined,
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!name.trim()) {
            setError('Please enter your name');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            // Filter out undefined values
            const cleanedData: any = {};
            Object.entries(perfData).forEach(([key, value]) => {
                if (value !== undefined && value !== null && value !== '') {
                    cleanedData[key] = value;
                }
            });

            const response = await fetch('/api/v1/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name.trim(),
                    performance_data: Object.keys(cleanedData).length > 0 ? cleanedData : null
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to create profile');
            }

            const data = await response.json();
            onProfileCreated(data.id, data.name);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const updatePerfData = (field: keyof PerformanceData, value: string) => {
        const numValue = value === '' ? undefined : parseFloat(value);
        setPerfData(prev => ({ ...prev, [field]: numValue }));
    };

    return (
        <div className="profile-form-container">
            <div className="profile-form-card">
                <h2>🎮 Create Your Profile</h2>
                <p className="subtitle">Enter your gaming/sports performance data to get personalized exercise recommendations</p>

                <form onSubmit={handleSubmit}>
                    <div className="form-section">
                        <h3>Basic Info</h3>
                        <div className="form-group">
                            <label htmlFor="name">Your Name *</label>
                            <input
                                id="name"
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="Enter your name"
                                required
                            />
                        </div>
                    </div>

                    <div className="form-section">
                        <h3>Gaming Performance</h3>
                        <div className="form-row">
                            <div className="form-group">
                                <label htmlFor="reaction_time">Reaction Time (ms)</label>
                                <input
                                    id="reaction_time"
                                    type="number"
                                    step="0.1"
                                    value={perfData.reaction_time ?? ''}
                                    onChange={(e) => updatePerfData('reaction_time', e.target.value)}
                                    placeholder="e.g., 250"
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="accuracy">Accuracy (%)</label>
                                <input
                                    id="accuracy"
                                    type="number"
                                    step="0.1"
                                    min="0"
                                    max="100"
                                    value={perfData.accuracy ?? ''}
                                    onChange={(e) => updatePerfData('accuracy', e.target.value)}
                                    placeholder="e.g., 85"
                                />
                            </div>
                        </div>
                        <div className="form-row">
                            <div className="form-group">
                                <label htmlFor="score">Game Score/Rating</label>
                                <input
                                    id="score"
                                    type="number"
                                    step="0.1"
                                    value={perfData.score ?? ''}
                                    onChange={(e) => updatePerfData('score', e.target.value)}
                                    placeholder="e.g., 2500"
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="playtime_hours">Playtime (hrs/week)</label>
                                <input
                                    id="playtime_hours"
                                    type="number"
                                    step="0.1"
                                    value={perfData.playtime_hours ?? ''}
                                    onChange={(e) => updatePerfData('playtime_hours', e.target.value)}
                                    placeholder="e.g., 20"
                                />
                            </div>
                        </div>
                    </div>

                    <div className="form-section">
                        <h3>Physical Performance (0-100)</h3>
                        <div className="form-row">
                            <div className="form-group">
                                <label htmlFor="endurance">Endurance</label>
                                <input
                                    id="endurance"
                                    type="number"
                                    min="0"
                                    max="100"
                                    value={perfData.endurance ?? ''}
                                    onChange={(e) => updatePerfData('endurance', e.target.value)}
                                    placeholder="0-100"
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="strength">Strength</label>
                                <input
                                    id="strength"
                                    type="number"
                                    min="0"
                                    max="100"
                                    value={perfData.strength ?? ''}
                                    onChange={(e) => updatePerfData('strength', e.target.value)}
                                    placeholder="0-100"
                                />
                            </div>
                        </div>
                        <div className="form-row">
                            <div className="form-group">
                                <label htmlFor="flexibility">Flexibility</label>
                                <input
                                    id="flexibility"
                                    type="number"
                                    min="0"
                                    max="100"
                                    value={perfData.flexibility ?? ''}
                                    onChange={(e) => updatePerfData('flexibility', e.target.value)}
                                    placeholder="0-100"
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="balance">Balance</label>
                                <input
                                    id="balance"
                                    type="number"
                                    min="0"
                                    max="100"
                                    value={perfData.balance ?? ''}
                                    onChange={(e) => updatePerfData('balance', e.target.value)}
                                    placeholder="0-100"
                                />
                            </div>
                        </div>
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" className="submit-btn" disabled={loading}>
                        {loading ? 'Creating Profile...' : '✨ Create Profile & Get Recommendations'}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default ProfileForm;
