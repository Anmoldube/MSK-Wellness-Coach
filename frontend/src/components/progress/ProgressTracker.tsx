import { useState, useEffect } from 'react';
import './ProgressTracker.css';

interface ProgressEntry {
    id: string;
    metric_name: string;
    metric_value: number;
    metric_unit: string | null;
    recorded_at: string;
    notes: string | null;
}

interface ProgressTrackerProps {
    userId: string;
}

function ProgressTracker({ userId }: ProgressTrackerProps) {
    const [progressData, setProgressData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [selectedMetric, setSelectedMetric] = useState<string | null>(null);
    const [trendData, setTrendData] = useState<any>(null);

    useEffect(() => {
        fetchProgressSummary();
    }, [userId]);

    useEffect(() => {
        if (selectedMetric) {
            fetchTrendData(selectedMetric);
        }
    }, [selectedMetric]);

    const fetchProgressSummary = async () => {
        try {
            const response = await fetch(`/api/v1/progress/${userId}/summary?days=30`);
            const data = await response.json();
            setProgressData(data);
            
            // Select first metric by default
            if (data.metrics_tracked && data.metrics_tracked.length > 0) {
                setSelectedMetric(data.metrics_tracked[0].metric_name);
            }
        } catch (error) {
            console.error('Error fetching progress:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchTrendData = async (metric: string) => {
        try {
            const response = await fetch(`/api/v1/progress/${userId}/trends?metric_name=${metric}&days=30`);
            const data = await response.json();
            setTrendData(data);
        } catch (error) {
            console.error('Error fetching trend data:', error);
        }
    };

    if (loading) {
        return <div className="progress-loading">Loading progress data...</div>;
    }

    if (!progressData || progressData.metrics_tracked.length === 0) {
        return (
            <div className="progress-empty">
                <h2>📈 No Progress Data Yet</h2>
                <p>Start tracking your metrics to see your improvement over time!</p>
            </div>
        );
    }

    const getTrendIcon = (trend: string) => {
        if (trend === 'improving') return '📈';
        if (trend === 'declining') return '📉';
        return '➡️';
    };

    const getTrendColor = (trend: string) => {
        if (trend === 'improving') return '#22c55e';
        if (trend === 'declining') return '#ef4444';
        return '#6b7280';
    };

    return (
        <div className="progress-tracker">
            <div className="progress-header">
                <h2>📊 Your Progress</h2>
                <p>Last 30 days • {progressData.total_entries} total entries</p>
            </div>

            <div className="metrics-grid">
                {progressData.metrics_tracked.map((metric: any) => (
                    <div
                        key={metric.metric_name}
                        className={`metric-card ${selectedMetric === metric.metric_name ? 'selected' : ''}`}
                        onClick={() => setSelectedMetric(metric.metric_name)}
                    >
                        <div className="metric-header">
                            <h3>{metric.metric_name.replace(/_/g, ' ')}</h3>
                            <span className="trend-icon">{getTrendIcon(metric.trend)}</span>
                        </div>
                        <div className="metric-value">
                            {metric.latest_value}
                            {metric.metric_unit && <span className="unit"> {metric.metric_unit}</span>}
                        </div>
                        {metric.improvement_percentage !== undefined && (
                            <div 
                                className="metric-change"
                                style={{ color: getTrendColor(metric.trend) }}
                            >
                                {metric.improvement_percentage > 0 ? '+' : ''}
                                {metric.improvement_percentage.toFixed(1)}% change
                            </div>
                        )}
                        <div className="metric-entries">{metric.total_entries} entries</div>
                    </div>
                ))}
            </div>

            {selectedMetric && trendData && (
                <div className="trend-detail">
                    <h3>📈 {selectedMetric.replace(/_/g, ' ')} Trend</h3>
                    
                    <div className="trend-stats">
                        <div className="stat-box">
                            <div className="stat-label">Current</div>
                            <div className="stat-value">
                                {trendData.current_value} {trendData.metric_unit}
                            </div>
                        </div>
                        <div className="stat-box">
                            <div className="stat-label">Starting</div>
                            <div className="stat-value">
                                {trendData.starting_value} {trendData.metric_unit}
                            </div>
                        </div>
                        <div className="stat-box">
                            <div className="stat-label">Average</div>
                            <div className="stat-value">
                                {trendData.average_value} {trendData.metric_unit}
                            </div>
                        </div>
                        <div className="stat-box">
                            <div className="stat-label">Improvement</div>
                            <div 
                                className="stat-value"
                                style={{ color: getTrendColor(trendData.trend) }}
                            >
                                {trendData.improvement_percentage > 0 ? '+' : ''}
                                {trendData.improvement_percentage}%
                            </div>
                        </div>
                    </div>

                    <div className="trend-chart">
                        <h4>Data Points</h4>
                        <div className="data-points">
                            {trendData.data_points.map((point: any, index: number) => (
                                <div key={index} className="data-point">
                                    <div className="point-date">
                                        {new Date(point.date).toLocaleDateString()}
                                    </div>
                                    <div className="point-value">
                                        {point.value} {trendData.metric_unit}
                                    </div>
                                    {point.notes && (
                                        <div className="point-notes">{point.notes}</div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ProgressTracker;
