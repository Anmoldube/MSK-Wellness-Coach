import { useState } from 'react';
import ChatInterface from './components/chat/ChatInterface';
import Sidebar from './components/chat/Sidebar';
import ReportDashboard from './components/dashboard/ReportDashboard';
import RecommendationList from './components/recommendations/RecommendationList';
import './App.css';

type View = 'chat' | 'reports' | 'recommendations' | 'progress';

function App() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [currentView, setCurrentView] = useState<View>('chat');

    const renderView = () => {
        switch (currentView) {
            case 'chat':
                return <ChatInterface />;
            case 'reports':
                return <ReportDashboard />;
            case 'recommendations':
                return <RecommendationList />;
            case 'progress':
                return (
                    <div className="coming-soon">
                        <h2>📈 Progress Tracking</h2>
                        <p>Coming soon! Track your improvement over time.</p>
                    </div>
                );
            default:
                return <ChatInterface />;
        }
    };

    return (
        <div className="app">
            {/* Header */}
            <header className="app-header">
                <button
                    className="menu-btn"
                    onClick={() => setSidebarOpen(!sidebarOpen)}
                    aria-label="Toggle menu"
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <line x1="3" y1="6" x2="21" y2="6" />
                        <line x1="3" y1="12" x2="21" y2="12" />
                        <line x1="3" y1="18" x2="21" y2="18" />
                    </svg>
                </button>

                <div className="app-logo">
                    <div className="logo-icon">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                            <path
                                d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"
                                fill="url(#logo-gradient)"
                            />
                            <defs>
                                <linearGradient id="logo-gradient" x1="2" y1="2" x2="22" y2="21" gradientUnits="userSpaceOnUse">
                                    <stop stopColor="#2ea3ff" />
                                    <stop offset="1" stopColor="#22c55e" />
                                </linearGradient>
                            </defs>
                        </svg>
                    </div>
                    <div className="logo-text">
                        <h1>MSK Wellness Coach</h1>
                        <span className="logo-subtitle">Your Personal Health Companion</span>
                    </div>
                </div>

                {/* View Tabs (visible on larger screens) */}
                <nav className="header-nav">
                    <button
                        className={`nav-tab ${currentView === 'chat' ? 'active' : ''}`}
                        onClick={() => setCurrentView('chat')}
                    >
                        💬 Chat
                    </button>
                    <button
                        className={`nav-tab ${currentView === 'reports' ? 'active' : ''}`}
                        onClick={() => setCurrentView('reports')}
                    >
                        📊 Reports
                    </button>
                    <button
                        className={`nav-tab ${currentView === 'recommendations' ? 'active' : ''}`}
                        onClick={() => setCurrentView('recommendations')}
                    >
                        💪 Exercises
                    </button>
                </nav>

                <div className="header-actions">
                    <button className="icon-btn" aria-label="Settings">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="3" />
                            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
                        </svg>
                    </button>
                </div>
            </header>

            {/* Main Content */}
            <div className="app-body">
                {/* Sidebar */}
                <Sidebar
                    isOpen={sidebarOpen}
                    onClose={() => setSidebarOpen(false)}
                />

                {/* Main View */}
                <main className="app-main">
                    {renderView()}
                </main>
            </div>
        </div>
    );
}

export default App;
