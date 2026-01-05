import { useState } from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { LoadingSpinner } from "./ui/LoadingSpinner";
import { MatchResults } from "./MatchResults";
import { Zap, ArrowRight } from "lucide-react";
import { toast } from "sonner";

interface MatchSectionProps {
  apiBase: string;
  jobId: string;
  setJobId: (id: string) => void;
  topK: number;
  isResumeIndexed: boolean;
}

export const MatchSection = ({
  apiBase,
  jobId,
  setJobId,
  topK,
  isResumeIndexed,
}: MatchSectionProps) => {
  const [isMatching, setIsMatching] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [rawOutput, setRawOutput] = useState<string | null>(null);

  const handleMatch = async () => {
    if (!jobId.trim()) return;

    setIsMatching(true);
    setResult(null);
    setRawOutput(null);

    try {
      const response = await fetch(`${apiBase}/job/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          job_id: jobId.trim(),
          top_k_resume: topK,
        }),
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();

      if (data.result) {
        setResult(data.result);
        toast.success("Match analysis complete!");
      } else {
        setRawOutput(data.raw_llm || JSON.stringify(data));
        toast.warning("Could not parse LLM response");
      }
    } catch (error) {
      toast.error(`Match failed: ${error}`);
    } finally {
      setIsMatching(false);
    }
  };

  const canMatch = jobId.trim() && isResumeIndexed;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/20 text-primary font-semibold text-sm">
          3
        </div>
        <div>
          <h2 className="font-semibold text-lg">Analyze Match</h2>
          <p className="text-sm text-muted-foreground">
            Get AI-powered insights on how well you fit the role
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Job ID</label>
          <Input
            value={jobId}
            onChange={(e) => setJobId(e.target.value)}
            placeholder="Enter job ID from step 2"
            className="input-field font-mono"
          />
        </div>

        {!isResumeIndexed && (
          <div className="glass-card p-4 border-amber-500/30 bg-amber-500/5">
            <p className="text-sm text-amber-400">
              Please index your resume first (Step 1) before running the match analysis.
            </p>
          </div>
        )}

        <Button
          onClick={handleMatch}
          disabled={!canMatch || isMatching}
          className="btn-primary w-full"
        >
          {isMatching ? (
            <>
              <LoadingSpinner size="sm" />
              <span className="ml-2">Analyzing with RAG + LLM...</span>
            </>
          ) : (
            <>
              <Zap className="w-4 h-4 mr-2" />
              Run Match Analysis
              <ArrowRight className="w-4 h-4 ml-2" />
            </>
          )}
        </Button>
      </div>

      {result && <MatchResults result={result} />}

      {rawOutput && (
        <div className="glass-card p-4 animate-fade-in">
          <h4 className="font-medium mb-3 text-amber-400">Raw LLM Output</h4>
          <pre className="text-xs font-mono bg-muted/50 p-3 rounded-lg overflow-x-auto text-muted-foreground">
            {rawOutput}
          </pre>
        </div>
      )}
    </div>
  );
};
