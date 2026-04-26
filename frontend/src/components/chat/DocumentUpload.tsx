import { useState, useRef, useEffect, useCallback } from 'react';
import { apiService } from '../../services/api.service';
import { UserDocument } from '../../types/chat.types';
import './DocumentUpload.css';

interface DocumentUploadProps {
    userId: string;
}

function DocumentUpload({ userId }: DocumentUploadProps) {
    const [documents, setDocuments] = useState<UserDocument[]>([]);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const loadDocuments = useCallback(async () => {
        if (!userId) return;
        try {
            const docs = await apiService.getUserDocuments(userId);
            setDocuments(docs as UserDocument[]);
        } catch (err) {
            console.error('Failed to load documents:', err);
        }
    }, [userId]);

    useEffect(() => {
        loadDocuments();
    }, [loadDocuments]);

    const handleUpload = async (file: File) => {
        setUploading(true);
        try {
            await apiService.uploadDocument(userId, file);
            await loadDocuments();
        } catch (err) {
            console.error('Upload failed:', err);
        } finally {
            setUploading(false);
        }
    };

    const handleDelete = async (docId: string) => {
        try {
            await apiService.deleteDocument(docId);
            setDocuments(prev => prev.filter(d => d.doc_id !== docId));
        } catch (err) {
            console.error('Delete failed:', err);
        }
    };

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') setDragActive(true);
        else if (e.type === 'dragleave') setDragActive(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setDragActive(false);
        if (e.dataTransfer.files?.[0]) {
            handleUpload(e.dataTransfer.files[0]);
        }
    };

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            handleUpload(e.target.files[0]);
            e.target.value = '';
        }
    };

    const getStatusBadge = (status: string) => {
        switch (status) {
            case 'indexed': return <span className="doc-badge doc-badge-success">Indexed</span>;
            case 'processing': return <span className="doc-badge doc-badge-pending">Processing…</span>;
            case 'failed': return <span className="doc-badge doc-badge-error">Failed</span>;
            default: return null;
        }
    };

    const getFileIcon = (fileType: string) => {
        switch (fileType) {
            case 'pdf': return '📄';
            case 'csv': return '📊';
            default: return '📝';
        }
    };

    return (
        <div className="doc-upload">
            {/* Drop Zone */}
            <div
                className={`doc-dropzone ${dragActive ? 'active' : ''} ${uploading ? 'uploading' : ''}`}
                onDragEnter={handleDrag}
                onDragOver={handleDrag}
                onDragLeave={handleDrag}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.txt,.csv"
                    onChange={handleFileInput}
                    style={{ display: 'none' }}
                />
                {uploading ? (
                    <div className="doc-uploading">
                        <div className="doc-spinner" />
                        <span>Indexing document…</span>
                    </div>
                ) : (
                    <>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                            <polyline points="17 8 12 3 7 8" />
                            <line x1="12" y1="3" x2="12" y2="15" />
                        </svg>
                        <span>Drop PDF, TXT, CSV here</span>
                        <span className="doc-dropzone-hint">or click to browse</span>
                    </>
                )}
            </div>

            {/* Document List */}
            <div className="doc-list">
                {documents.length === 0 && (
                    <div className="doc-empty">No documents uploaded yet</div>
                )}
                {documents.map(doc => (
                    <div key={doc.doc_id} className="doc-item">
                        <span className="doc-icon">{getFileIcon(doc.file_type)}</span>
                        <div className="doc-item-info">
                            <span className="doc-name">{doc.filename}</span>
                            <span className="doc-meta">
                                {doc.page_count} pages · {doc.chunk_count} chunks
                            </span>
                        </div>
                        {getStatusBadge(doc.status)}
                        <button
                            className="doc-item-delete"
                            onClick={() => handleDelete(doc.doc_id)}
                            title="Remove document"
                        >
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <line x1="18" y1="6" x2="6" y2="18" />
                                <line x1="6" y1="6" x2="18" y2="18" />
                            </svg>
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default DocumentUpload;
