import { useState, useRef } from 'react';
import './FileUpload.css';

interface FileUploadProps {
    onUpload: (file: File) => void;
    accept?: string;
    maxSizeMB?: number;
}

function FileUpload({
    onUpload,
    accept = '.json,.csv,.pdf',
    maxSizeMB = 10
}: FileUploadProps) {
    const [dragActive, setDragActive] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [uploading, setUploading] = useState(false);
    const [success, setSuccess] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (file: File) => {
        setError(null);
        setSuccess(false);

        // Validate file size
        if (file.size > maxSizeMB * 1024 * 1024) {
            setError(`File too large. Maximum size is ${maxSizeMB}MB`);
            return;
        }

        // Validate file type
        const validTypes = accept.split(',').map(t => t.trim());
        const fileExt = '.' + file.name.split('.').pop()?.toLowerCase();
        if (!validTypes.some(t => t === fileExt || t === file.type)) {
            setError(`Invalid file type. Accepted: ${accept}`);
            return;
        }

        setSelectedFile(file);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setUploading(true);
        setError(null);

        try {
            await onUpload(selectedFile);
            setSuccess(true);
            setSelectedFile(null);
        } catch (err) {
            setError('Failed to upload file. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    const handleRemove = () => {
        setSelectedFile(null);
        setError(null);
        setSuccess(false);
        if (inputRef.current) {
            inputRef.current.value = '';
        }
    };

    return (
        <div className="file-upload">
            <div
                className={`drop-zone ${dragActive ? 'active' : ''} ${selectedFile ? 'has-file' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current?.click()}
            >
                <input
                    ref={inputRef}
                    type="file"
                    accept={accept}
                    onChange={handleChange}
                    hidden
                />

                {selectedFile ? (
                    <div className="selected-file">
                        <div className="file-icon">
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                                <polyline points="14,2 14,8 20,8" />
                            </svg>
                        </div>
                        <div className="file-info">
                            <span className="file-name">{selectedFile.name}</span>
                            <span className="file-size">
                                {(selectedFile.size / 1024).toFixed(1)} KB
                            </span>
                        </div>
                        <button
                            className="remove-btn"
                            onClick={(e) => { e.stopPropagation(); handleRemove(); }}
                            aria-label="Remove file"
                        >
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <line x1="18" y1="6" x2="6" y2="18" />
                                <line x1="6" y1="6" x2="18" y2="18" />
                            </svg>
                        </button>
                    </div>
                ) : (
                    <div className="drop-content">
                        <div className="upload-icon">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                                <polyline points="17,8 12,3 7,8" />
                                <line x1="12" y1="3" x2="12" y2="15" />
                            </svg>
                        </div>
                        <p className="drop-text">
                            <strong>Click to upload</strong> or drag and drop
                        </p>
                        <p className="file-types">
                            {accept.replace(/\./g, '').toUpperCase()} files up to {maxSizeMB}MB
                        </p>
                    </div>
                )}
            </div>

            {error && (
                <div className="upload-error">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
                    </svg>
                    {error}
                </div>
            )}

            {success && (
                <div className="upload-success">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                    </svg>
                    File uploaded successfully!
                </div>
            )}

            {selectedFile && !success && (
                <button
                    className="upload-btn"
                    onClick={handleUpload}
                    disabled={uploading}
                >
                    {uploading ? (
                        <>
                            <div className="btn-spinner"></div>
                            Uploading...
                        </>
                    ) : (
                        'Upload Report'
                    )}
                </button>
            )}
        </div>
    );
}

export default FileUpload;
