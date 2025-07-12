import { Button } from "@/components/ui/button";
import { Menu, Github, ExternalLink } from "lucide-react";

interface HeaderProps {
  onMenuToggle: () => void;
}

export const Header = ({ onMenuToggle }: HeaderProps) => {
  return (
    <header className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container flex h-14 sm:h-16 items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-2 sm:gap-4 min-w-0">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={onMenuToggle}
            className="md:hidden h-8 w-8 p-0"
          >
            <Menu className="h-4 w-4" />
          </Button>
          <div className="flex items-center gap-2 sm:gap-3 min-w-0">
            <div className="w-6 h-6 sm:w-8 rounded-lg flex items-center justify-center flex-shrink-0">
              <img src="/favicon.ico" alt="" style={{borderRadius:'5px'}}/>
            </div>
            <div className="min-w-0">
              <h1 className="text-base sm:text-lg lg:text-xl font-bold bg-gradient-primary bg-clip-text text-transparent truncate">
                AI Scheduling Assistant
              </h1>
              <p className="text-xs text-muted-foreground hidden sm:block">AMD Hackathon 2025</p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
          <Button variant="outline" size="sm" asChild className="h-8 px-2 sm:px-3">
            <a 
              href="https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-1 sm:gap-2"
            >
              <Github className="h-3 w-3 sm:h-4 sm:w-4" />
              <span className="hidden sm:inline text-xs sm:text-sm">GitHub</span>
            </a>
          </Button>
          <Button size="sm" className="bg-gradient-primary hover:opacity-90 h-8 px-2 sm:px-3">
            <a href="https://lu.ma/wpodf9j9" className="flex" target="_blank" rel="noopener noreferrer">
              <ExternalLink className="h-3 w-3 sm:h-4 sm:w-4 sm:mr-2" />
              <span className="hidden sm:inline text-xs sm:text-sm">AMD Cloud</span>
            </a>
          </Button>
        </div>
      </div>
    </header>
  );
};