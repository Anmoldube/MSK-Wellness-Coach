import { useState, useEffect } from 'react';
import { apiService } from '../../services/api.service';
import './ReportDashboard.css';

interface Parameter {
    parameter_name: string;
    parameter_category: string;
    value: number;
    unit: string;
    percentile?: number;
    interpretation?: string;
    reference_range_min?: number;
    reference_range_max?: number;
}

interface Report {
    report_id: string;
    assessment_date: string;
    overall_score: number;
    risk_level: string;
    parameters: Parameter[];
}

function ReportDashboard() {
    const [report, setReport] = useState<Report | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadReport();
    }, []);

    const loadReport = async () => {
        try {
            setLoading(true);
            const data = await apiService.getLatestReport();
            setReport(data);
        } catch (err) {
            setError('Failed to load report');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="dashboard-loading">
                <div className="loading-spinner-lg"></div>
                <p>Loading your assessment...</p>
            </div>
        );
    }

    if (error || !report) {
        return (
            <div className="dashboard-error">
                <p>{error || 'No report available'}</p>
                <button onClick={loadReport}>Try Again</button>
            </div>
        );
    }

    const getRiskColor = (level: string) => {
        switch (level.toLowerCase()) {
            case 'low': return 'var(--secondary-500)';
            case 'moderate': return 'var(--primary-500)';
            case 'high': return 'var(--accent-500)';
            default: return 'var(--neutral-400)';
        }
    };

    const getScoreColor = (percentile: number) => {
        if (percentile >= 70) return 'score-good';
        if (percentile >= 40) return 'score-moderate';
        return 'score-poor';
    };

    const groupedParams = report.parameters.reduce((acc, param) => {
        const category = param.parameter_category;
        if (!acc[category]) acc[category] = [];
        acc[category].push(param);
        return acc;
    }, {} as Record<string, Parameter[]>);

    return (
        <div className="report-dashboard">
            {/* Header */}
            <div className="dashboard-header">
                <div className="header-info">
                    <h2>MSK Assessment Report</h2>
                    <span className="assessment-date">
                        {new Date(report.assessment_date).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                        })}
                    </span>
                </div>

                {/* Overall Score */}
                <div className="overall-score-card">
                    <div className="score-circle">
                        <svg viewBox="0 0 100 100">
                            <circle
                                cx="50"
                                cy="50"
                                r="45"
                                fill="none"
                                stroke="var(--neutral-700)"
                                strokeWidth="8"
                            />
                            <circle
                                cx="50"
                                cy="50"
                                r="45"
                                fill="none"
                                stroke={getRiskColor(report.risk_level)}
                                strokeWidth="8"
                                strokeLinecap="round"
                                strokeDasharray={`${(report.overall_score / 100) * 283} 283`}
                                transform="rotate(-90 50 50)"
                            />
                        </svg>
                        <div className="score-value">
                            <span className="score-number">{report.overall_score}</span>
                            <span className="score-max">/100</span>
                        </div>
                    </div>
                    <div className="risk-badge" style={{ backgroundColor: getRiskColor(report.risk_level) }}>
                        {report.risk_level.toUpperCase()} RISK
                    </div>
                </div>
            </div>

            {/* Parameters Grid */}
            <div className="parameters-grid">
                {Object.entries(groupedParams).map(([category, params]) => (
                    <div key={category} className="category-section">
                        <h3 className="category-title">
                            {category.replace('_', ' ').toUpperCase()}
                        </h3>
                        <div className="params-list">
                            {params.map((param) => (
                                <div key={param.parameter_name} className="param-card">
                                    <div className="param-header">
                                        <span className="param-name">
                                            {param.parameter_name.replace(/_/g, ' ')}
                                        </span>
                                        {param.percentile && (
                                            <span className={`param-percentile ${getScoreColor(param.percentile)}`}>
                                                {param.percentile}th
                                            </span>
                                        )}
                                    </div>
                                    <div className="param-value">
                                        <span className="value">{param.value}</span>
                                        <span className="unit">{param.unit}</span>
                                    </div>
                                    {param.interpretation && (
                                        <div className="param-interpretation">
                                            {param.interpretation}
                                        </div>
                                    )}
                                    {param.reference_range_min && param.reference_range_max && (
                                        <div className="param-range">
                                            Range: {param.reference_range_min} - {param.reference_range_max} {param.unit}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            {/* Quick Actions */}
            <div className="dashboard-actions">
                <button className="action-btn primary">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
                    </svg>
                    Discuss with Coach
                </button>
                <button className="action-btn secondary">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 20h9M16.5 3.5a2.12 2.12 0 013 3L7 19l-4 1 1-4L16.5 3.5z" />
                    </svg>
                    Get Exercises
                </button>
                <button className="action-btn secondary">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                        <line x1="16" y1="2" x2="16" y2="6" />
                        <line x1="8" y1="2" x2="8" y2="6" />
                        <line x1="3" y1="10" x2="21" y2="10" />
                    </svg>
                    Find Programs
                </button>
            </div>
        </div>
    );
}

export default ReportDashboard;
