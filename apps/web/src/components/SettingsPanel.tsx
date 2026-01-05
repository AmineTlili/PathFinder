import { X, Server, Sliders } from "lucide-react";
import { Input } from "./ui/input";
import { Slider } from "./ui/slider";

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  apiBase: string;
  setApiBase: (value: string) => void;
  topK: number;
  setTopK: (value: number) => void;
}

export const SettingsPanel = ({
  isOpen,
  onClose,
  apiBase,
  setApiBase,
  topK,
  setTopK,
}: SettingsPanelProps) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div className="absolute inset-0 bg-background/80 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-md glass-card-elevated h-full animate-slide-up border-l border-border/50">
        <div className="p-6 border-b border-border/50 flex items-center justify-between">
          <h2 className="font-semibold text-lg">Settings</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-muted rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-8">
          {/* API Configuration */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Server className="w-4 h-4 text-primary" />
              <span className="section-title mb-0">API Configuration</span>
            </div>
            <div className="space-y-3">
              <label className="text-sm font-medium">Base URL</label>
              <Input
                value={apiBase}
                onChange={(e) => setApiBase(e.target.value)}
                placeholder="http://127.0.0.1:8000"
                className="input-field"
              />
              <p className="text-xs text-muted-foreground">
                Make sure your API server is running at this address
              </p>
            </div>
          </div>

          {/* RAG Settings */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Sliders className="w-4 h-4 text-primary" />
              <span className="section-title mb-0">RAG Settings</span>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Top K Resume Chunks</label>
                <span className="text-sm font-mono text-primary">{topK}</span>
              </div>
              <Slider
                value={[topK]}
                onValueChange={(value) => setTopK(value[0])}
                min={3}
                max={10}
                step={1}
                className="w-full"
              />
              <p className="text-xs text-muted-foreground">
                Number of resume chunks to retrieve for matching
              </p>
            </div>
          </div>

          {/* Server Command */}
          <div className="glass-card p-4">
            <p className="text-sm text-muted-foreground mb-2">Start your API server:</p>
            <code className="text-xs font-mono text-primary bg-muted/50 p-2 rounded block">
              python -m uvicorn main:app --reload --port 8000
            </code>
          </div>
        </div>
      </div>
    </div>
  );
};
