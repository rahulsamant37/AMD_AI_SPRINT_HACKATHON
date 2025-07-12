import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CodeBlock } from "../CodeBlock";
import { 
  Server, 
  ExternalLink, 
  Cpu, 
  HardDrive, 
  Zap, 
  AlertCircle,
  CheckCircle2
} from "lucide-react";

export const SetupSection = () => {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl sm:text-3xl font-bold mb-3 sm:mb-4 bg-gradient-primary bg-clip-text text-transparent">
          Setup & Requirements
        </h2>
        <p className="text-muted-foreground text-base sm:text-lg">
          Get your development environment ready with AMD MI300X GPU and required tools.
        </p>
      </div>

      {/* Requirements Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <Cpu className="h-5 w-5 text-accent" />
            </div>
            Tools & APIs Required
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
            <div className="text-center p-3 sm:p-4 rounded-lg bg-muted/50 border border-border/50">
              <Server className="h-6 w-6 sm:h-8 sm:w-8 mx-auto mb-2 sm:mb-3 text-accent" />
              <h4 className="font-semibold mb-1 text-sm sm:text-base">vLLM Server</h4>
              <p className="text-xs sm:text-sm text-muted-foreground">MI300 GPU</p>
            </div>
            <div className="text-center p-3 sm:p-4 rounded-lg bg-muted/50 border border-border/50">
              <HardDrive className="h-6 w-6 sm:h-8 sm:w-8 mx-auto mb-2 sm:mb-3 text-ai-blue" />
              <h4 className="font-semibold mb-1 text-sm sm:text-base">Calendar APIs</h4>
              <p className="text-xs sm:text-sm text-muted-foreground">Google Calendar</p>
            </div>
            <div className="text-center p-3 sm:p-4 rounded-lg bg-muted/50 border border-border/50">
              <Zap className="h-6 w-6 sm:h-8 sm:w-8 mx-auto mb-2 sm:mb-3 text-ai-purple" />
              <h4 className="font-semibold mb-1 text-sm sm:text-base">Framework</h4>
              <p className="text-xs sm:text-sm text-muted-foreground">Python</p>
            </div>
            <div className="text-center p-3 sm:p-4 rounded-lg bg-muted/50 border border-border/50">
              <CheckCircle2 className="h-6 w-6 sm:h-8 sm:w-8 mx-auto mb-2 sm:mb-3 text-ai-cyan" />
              <h4 className="font-semibold mb-1 text-sm sm:text-base">License</h4>
              <p className="text-xs sm:text-sm text-muted-foreground">Free Tools</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* AMD Developer Cloud Setup */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-secondary/10">
              <Server className="h-5 w-5 text-ai-blue" />
            </div>
            AMD Developer Cloud Setup
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 sm:space-y-6">
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertDescription className="text-sm">
              Follow the detailed setup guide in the AMD Developer Cloud Setup README for complete instructions.
            </AlertDescription>
          </Alert>

          <div className="space-y-3 sm:space-y-4">
            <h4 className="font-semibold text-foreground flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center text-xs font-bold text-accent">1</span>
              Select GPU Droplets
            </h4>
            <p className="text-muted-foreground ml-8">Navigate to the GPU Droplets section in your AMD Developer Cloud dashboard.</p>

            <h4 className="font-semibold text-foreground flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center text-xs font-bold text-accent">2</span>
              Create GPU Droplets
            </h4>
            <p className="text-muted-foreground ml-8">Click on "Create GPU Droplets" to start the setup process.</p>

            <h4 className="font-semibold text-foreground flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center text-xs font-bold text-accent">3</span>
              Select AMD MI300X
            </h4>
            <p className="text-muted-foreground ml-8">Choose the AMD MI300X GPU configuration for optimal performance.</p>

            <h4 className="font-semibold text-foreground flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center text-xs font-bold text-accent">4</span>
              Choose Snapshot
            </h4>
            <div className="ml-8">
              <p className="text-muted-foreground mb-2">In Snapshots, select:</p>
              <Badge className="bg-accent/10 text-accent border-accent/20">
                Ubuntu_AMD_Hackathon_AI_Scheduling_Assistant
              </Badge>
            </div>

            <h4 className="font-semibold text-foreground flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center text-xs font-bold text-accent">5</span>
              Configure SSH Keys
            </h4>
            <p className="text-muted-foreground ml-8">Create and add your SSH keys for secure access.</p>

            <h4 className="font-semibold text-foreground flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center text-xs font-bold text-accent">6</span>
              Access Web Console
            </h4>
            <p className="text-muted-foreground ml-8">
              Open Web Console, copy the URL, paste it in Chrome, and use the provided Jupyter Token.
            </p>
          </div>

          <div className="pt-3 sm:pt-4">
            <Button className="bg-gradient-primary hover:opacity-90 w-full sm:w-auto" asChild>
              <a 
                href="https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/AMD_Developer_Cloud_Setup.md" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-2 justify-center"
              >
                <ExternalLink className="h-4 w-4" />
                <span className="text-sm sm:text-base">View Complete Setup Guide</span>
              </a>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Environment Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-accent/10">
              <Zap className="h-5 w-5 text-ai-cyan" />
            </div>
            Development Environment
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <div className="space-y-2 sm:space-y-3">
              <h4 className="font-semibold text-accent">Hardware</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• AMD MI300X GPU</li>
                <li>• High-memory configuration</li>
                <li>• Optimized for AI workloads</li>
              </ul>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold text-accent">Software Stack</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Python environment</li>
                <li>• vLLM inference server</li>
                <li>• Jupyter notebooks</li>
                <li>• Google Calendar API</li>
              </ul>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold text-accent">Models Available</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• DeepSeek LLM 7B Chat</li>
                <li>• Meta-Llama-3.1-8B-Instruct</li>
                <li>• Optimized for inference</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};