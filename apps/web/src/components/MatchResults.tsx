import { ScoreRing } from "./ui/ScoreRing";
import { CheckCircle, AlertTriangle, Lightbulb, FileSearch, ChevronDown } from "lucide-react";
import { useState } from "react";

interface MatchResultsProps {
  result: {
    match_score: number;
    strong_matches: string[];
    missing_skills: string[];
    recommended_actions: string[];
    evidence: Record<string, any>;
    notes: string;
  };
}

export const MatchResults = ({ result }: MatchResultsProps) => {
  const [showEvidence, setShowEvidence] = useState(false);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Score Section */}
      <div className="glass-card-elevated p-8 flex flex-col items-center">
        <ScoreRing score={result.match_score} />
      </div>

      {/* Skills Grid */}
      <div className="grid md:grid-cols-2 gap-4">
        {/* Strong Matches */}
        <div className="glass-card p-5">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5 text-primary" />
            <h3 className="font-semibold">Strong Matches</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {result.strong_matches.map((skill, idx) => (
              <span key={idx} className="tag-skill tag-skill-success">
                {skill}
              </span>
            ))}
            {result.strong_matches.length === 0 && (
              <p className="text-sm text-muted-foreground">No strong matches found</p>
            )}
          </div>
        </div>

        {/* Missing Skills */}
        <div className="glass-card p-5">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <h3 className="font-semibold">Skills to Develop</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {result.missing_skills.map((skill, idx) => (
              <span key={idx} className="tag-skill tag-skill-warning">
                {skill}
              </span>
            ))}
            {result.missing_skills.length === 0 && (
              <p className="text-sm text-muted-foreground">No skill gaps identified</p>
            )}
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="glass-card p-5">
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb className="w-5 h-5 text-primary" />
          <h3 className="font-semibold">Recommended Actions</h3>
        </div>
        <ul className="space-y-3">
          {result.recommended_actions.map((action, idx) => (
            <li key={idx} className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/20 text-primary text-xs font-medium flex items-center justify-center">
                {idx + 1}
              </span>
              <span className="text-sm text-muted-foreground">{action}</span>
            </li>
          ))}
          {result.recommended_actions.length === 0 && (
            <p className="text-sm text-muted-foreground">No specific recommendations</p>
          )}
        </ul>
      </div>

      {/* Notes */}
      {result.notes && (
        <div className="glass-card p-5">
          <h3 className="font-semibold mb-3">Analysis Notes</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{result.notes}</p>
        </div>
      )}

      {/* Evidence Collapsible */}
      <div className="glass-card overflow-hidden">
        <button
          onClick={() => setShowEvidence(!showEvidence)}
          className="w-full p-5 flex items-center justify-between hover:bg-muted/30 transition-colors"
        >
          <div className="flex items-center gap-2">
            <FileSearch className="w-5 h-5 text-muted-foreground" />
            <h3 className="font-semibold">Evidence & Sources</h3>
          </div>
          <ChevronDown
            className={`w-5 h-5 text-muted-foreground transition-transform ${
              showEvidence ? "rotate-180" : ""
            }`}
          />
        </button>
        {showEvidence && (
          <div className="p-5 pt-0 border-t border-border/50">
            <pre className="text-xs font-mono bg-muted/50 p-4 rounded-lg overflow-x-auto text-muted-foreground">
              {JSON.stringify(result.evidence, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};
