import { useState } from "react";
import { FileUpload } from "./ui/FileUpload";
import { LoadingSpinner } from "./ui/LoadingSpinner";
import { Button } from "./ui/button";
import { Sparkles, FileText, CheckCircle } from "lucide-react";
import { toast } from "sonner";

interface ResumeSectionProps {
  apiBase: string;
  onIndexed: () => void;
  isIndexed: boolean;
}

export const ResumeSection = ({ apiBase, onIndexed, isIndexed }: ResumeSectionProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [isIndexing, setIsIndexing] = useState(false);
  const [isParsing, setIsParsing] = useState(false);
  const [parseResult, setParseResult] = useState<any>(null);

  const handleIndex = async () => {
    if (!file) return;

    setIsIndexing(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${apiBase}/rag/index_resume`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      toast.success("Resume indexed successfully!");
      onIndexed();
    } catch (error) {
      toast.error(`Failed to index resume: ${error}`);
    } finally {
      setIsIndexing(false);
    }
  };

  const handleParse = async () => {
    if (!file) return;

    setIsParsing(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${apiBase}/resume/parse`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();
      setParseResult(data);
      toast.success("Resume parsed successfully!");
    } catch (error) {
      toast.error(`Failed to parse resume: ${error}`);
    } finally {
      setIsParsing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/20 text-primary font-semibold text-sm">
          1
        </div>
        <div>
          <h2 className="font-semibold text-lg">Upload Your Resume</h2>
          <p className="text-sm text-muted-foreground">
            Upload your CV to analyze against job opportunities
          </p>
        </div>
      </div>

      <FileUpload
        file={file}
        onFileSelect={setFile}
        onClear={() => {
          setFile(null);
          setParseResult(null);
        }}
        isIndexed={isIndexed}
      />

      <div className="flex gap-3">
        <Button
          onClick={handleIndex}
          disabled={!file || isIndexing}
          className="btn-primary flex-1"
        >
          {isIndexing ? (
            <LoadingSpinner size="sm" />
          ) : isIndexed ? (
            <>
              <CheckCircle className="w-4 h-4 mr-2" />
              Indexed
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 mr-2" />
              Index Resume
            </>
          )}
        </Button>

        <Button
          onClick={handleParse}
          disabled={!file || isParsing}
          variant="outline"
          className="btn-secondary"
        >
          {isParsing ? (
            <LoadingSpinner size="sm" />
          ) : (
            <>
              <FileText className="w-4 h-4 mr-2" />
              Preview
            </>
          )}
        </Button>
      </div>

      {parseResult && (
        <div className="glass-card p-4 animate-fade-in">
          <h4 className="font-medium mb-3 text-sm">Resume Structure</h4>
          <pre className="text-xs font-mono bg-muted/50 p-3 rounded-lg overflow-x-auto text-muted-foreground max-h-60 overflow-y-auto">
            {JSON.stringify(parseResult, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};
