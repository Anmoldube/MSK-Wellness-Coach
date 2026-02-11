/**
 * API Service for communicating with the backend
 */

const API_BASE_URL = '/api/v1';

interface ChatRequest {
    message: string;
    conversation_id?: string;
    include_context?: boolean;
    user_id?: string;
}

interface ChatResponse {
    message: string;
    conversation_id: string;
    function_calls?: Array<{
        name: string;
        arguments: Record<string, unknown>;
        result?: Record<string, unknown>;
    }>;
    citations?: string[];
    suggested_questions?: string[];
}

interface AssessmentReport {
    report_id: string;
    user_id: string;
    assessment_date: string;
    overall_score: number;
    risk_level: string;
    parameters: Array<{
        parameter_name: string;
        parameter_category: string;
        value: number;
        unit: string;
        percentile?: number;
        interpretation?: string;
    }>;
}

class ApiService {
    private baseUrl: string;

    constructor() {
        this.baseUrl = API_BASE_URL;
    }

    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;

        const defaultHeaders: HeadersInit = {
            'Content-Type': 'application/json',
        };

        const response = await fetch(url, {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers,
            },
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP error ${response.status}`);
        }

        return response.json();
    }

    // Chat endpoints
    async sendMessage(request: ChatRequest): Promise<ChatResponse> {
        return this.request<ChatResponse>('/chat/message', {
            method: 'POST',
            body: JSON.stringify(request),
        });
    }

    async getConversations(limit: number = 10) {
        return this.request<Array<{
            conversation_id: string;
            started_at: string;
            message_count: number;
        }>>(`/chat/conversations?limit=${limit}`);
    }

    // Reports endpoints
    async getLatestReport(): Promise<AssessmentReport> {
        return this.request<AssessmentReport>('/reports/latest');
    }

    async getReports(limit: number = 10) {
        return this.request<Array<{
            report_id: string;
            assessment_date: string;
            overall_score: number;
            risk_level: string;
        }>>(`/reports?limit=${limit}`);
    }

    // Recommendations endpoints
    async getCarePrograms(focusAreas?: string[]) {
        const params = focusAreas ? `?focus_areas=${focusAreas.join(',')}` : '';
        return this.request(`/recommendations/care-programs${params}`);
    }

    async getExercises(targetParameter?: string) {
        const params = targetParameter ? `?target_parameter=${targetParameter}` : '';
        return this.request(`/recommendations/exercises${params}`);
    }

    async getProducts(condition?: string) {
        const params = condition ? `?condition=${condition}` : '';
        return this.request(`/recommendations/products${params}`);
    }

    // Health check
    async healthCheck(): Promise<{ status: string }> {
        const response = await fetch('/health');
        return response.json();
    }
}

export const apiService = new ApiService();
export default apiService;
