import { useState, useCallback } from "react";
import { Upload, FileText, X, CheckCircle } from "lucide-react";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  file: File | null;
  onClear: () => void;
  accept?: string;
  isIndexed?: boolean;
}

export const FileUpload = ({ 
  onFileSelect, 
  file, 
  onClear, 
  accept = ".pdf",
  isIndexed = false 
}: FileUploadProps) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      onFileSelect(files[0]);
    }
  }, [onFileSelect]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onFileSelect(files[0]);
    }
  };

  if (file) {
    return (
      <div className={`glass-card p-4 flex items-center gap-4 ${isIndexed ? 'border-primary/50' : ''}`}>
        <div className={`p-3 rounded-lg ${isIndexed ? 'bg-primary/20' : 'bg-muted'}`}>
          {isIndexed ? (
            <CheckCircle className="w-6 h-6 text-primary" />
          ) : (
            <FileText className="w-6 h-6 text-muted-foreground" />
          )}
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-medium truncate">{file.name}</p>
          <p className="text-sm text-muted-foreground">
            {isIndexed ? 'Indexed & Ready' : `${(file.size / 1024).toFixed(1)} KB`}
          </p>
        </div>
        <button
          onClick={onClear}
          className="p-2 hover:bg-muted rounded-lg transition-colors"
        >
          <X className="w-5 h-5 text-muted-foreground" />
        </button>
      </div>
    );
  }

  return (
    <label
      className={`upload-zone p-8 flex flex-col items-center gap-4 cursor-pointer ${
        isDragging ? 'dragging' : ''
      }`}
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        className="hidden"
        accept={accept}
        onChange={handleChange}
      />
      <div className="p-4 rounded-full bg-muted/50">
        <Upload className="w-8 h-8 text-muted-foreground" />
      </div>
      <div className="text-center">
        <p className="font-medium">
          Drop your resume here or <span className="text-primary">browse</span>
        </p>
        <p className="text-sm text-muted-foreground mt-1">
          Supports PDF files up to 10MB
        </p>
      </div>
    </label>
  );
};
