import { useState } from "react";
import { Header } from "@/components/Header";
import { SettingsPanel } from "@/components/SettingsPanel";
import { ResumeSection } from "@/components/ResumeSection";
import { JobSection } from "@/components/JobSection";
import { MatchSection } from "@/components/MatchSection";
import { Sparkles } from "lucide-react";

const Index = () => {
  const DEFAULT_API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
  const [apiBase, setApiBase] = useState(DEFAULT_API);
  const [topK, setTopK] = useState(6);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isResumeIndexed, setIsResumeIndexed] = useState(false);
  const [jobId, setJobId] = useState("");

  return (
    <div className="min-h-screen bg-background">
      <Header onSettingsClick={() => setIsSettingsOpen(true)} />

      <SettingsPanel
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        apiBase={apiBase}
        setApiBase={setApiBase}
        topK={topK}
        setTopK={setTopK}
      />

      {/* Hero Section */}
      <section className="relative overflow-hidden border-b border-border/50">
        <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent" />
        <div className="absolute top-20 left-1/4 w-72 h-72 bg-primary/10 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute top-40 right-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: "1s" }} />
        
        <div className="container mx-auto px-4 py-16 md:py-24 relative">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-sm text-primary animate-fade-in">
              <Sparkles className="w-4 h-4" />
              Powered by RAG + LLM Technology
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight animate-fade-in" style={{ animationDelay: "0.1s" }}>
              Match Your Skills to{" "}
              <span className="gradient-text">Dream Jobs</span>
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto animate-fade-in" style={{ animationDelay: "0.2s" }}>
              Upload your resume, paste any job description, and get an explainable 
              match score with AI-powered evidence and actionable recommendations.
            </p>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto space-y-12">
          {/* Step 1: Resume */}
          <div className="glass-card p-6 md:p-8 animate-slide-up">
            <ResumeSection
              apiBase={apiBase}
              onIndexed={() => setIsResumeIndexed(true)}
              isIndexed={isResumeIndexed}
            />
          </div>

          {/* Step 2: Job */}
          <div className="glass-card p-6 md:p-8 animate-slide-up" style={{ animationDelay: "0.1s" }}>
            <JobSection
              apiBase={apiBase}
              onJobUploaded={setJobId}
              jobId={jobId}
            />
          </div>

          {/* Step 3: Match */}
          <div className="glass-card p-6 md:p-8 animate-slide-up" style={{ animationDelay: "0.2s" }}>
            <MatchSection
              apiBase={apiBase}
              jobId={jobId}
              setJobId={setJobId}
              topK={topK}
              isResumeIndexed={isResumeIndexed}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 py-8 mt-12">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>PathFinder — AI-Powered Resume & Job Matching</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
