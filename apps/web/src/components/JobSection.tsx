import { useState } from "react";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { Button } from "./ui/button";
import { LoadingSpinner } from "./ui/LoadingSpinner";
import { Upload, CheckCircle, Briefcase, Building2, MapPin } from "lucide-react";
import { toast } from "sonner";

interface JobSectionProps {
  apiBase: string;
  onJobUploaded: (jobId: string) => void;
  jobId: string;
}

export const JobSection = ({ apiBase, onJobUploaded, jobId }: JobSectionProps) => {
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async () => {
    if (!description.trim()) return;

    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append("title", title);
      formData.append("company", company);
      formData.append("location", location);
      formData.append("description", description);

      const response = await fetch(`${apiBase}/job/upload_text`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();
      onJobUploaded(data.job_id);
      toast.success("Job offer indexed successfully!");
    } catch (error) {
      toast.error(`Failed to upload job: ${error}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/20 text-primary font-semibold text-sm">
          2
        </div>
        <div>
          <h2 className="font-semibold text-lg">Add Job Opportunity</h2>
          <p className="text-sm text-muted-foreground">
            Paste the job description you want to match against
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="grid md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-muted-foreground" />
              Job Title
            </label>
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., Senior Software Engineer"
              className="input-field"
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <Building2 className="w-4 h-4 text-muted-foreground" />
              Company
            </label>
            <Input
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              placeholder="e.g., Acme Inc."
              className="input-field"
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <MapPin className="w-4 h-4 text-muted-foreground" />
              Location
            </label>
            <Input
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g., Paris, France"
              className="input-field"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Job Description</label>
          <Textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Paste the complete job description here..."
            className="input-field min-h-[200px] resize-none"
          />
        </div>

        <Button
          onClick={handleUpload}
          disabled={!description.trim() || isUploading}
          className="btn-primary w-full"
        >
          {isUploading ? (
            <LoadingSpinner size="sm" />
          ) : jobId ? (
            <>
              <CheckCircle className="w-4 h-4 mr-2" />
              Job Indexed
            </>
          ) : (
            <>
              <Upload className="w-4 h-4 mr-2" />
              Upload & Index Job
            </>
          )}
        </Button>

        {jobId && (
          <div className="glass-card p-3 flex items-center gap-3 animate-fade-in">
            <CheckCircle className="w-5 h-5 text-primary flex-shrink-0" />
            <div className="min-w-0">
              <p className="text-sm font-medium">Job indexed successfully</p>
              <p className="text-xs font-mono text-muted-foreground truncate">
                ID: {jobId}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
