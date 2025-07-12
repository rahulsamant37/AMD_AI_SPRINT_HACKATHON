import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import { 
  BookOpen, 
  Settings, 
  Calendar, 
  Server, 
  Bot, 
  FileJson, 
  Trophy,
  X,
  ChevronRight
} from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  activeSection: string;
  onSectionChange: (section: string) => void;
}

const navItems = [
  { id: "introduction", label: "Introduction", icon: BookOpen },
  { id: "setup", label: "Setup & Requirements", icon: Settings },
  { id: "calendar", label: "Google Calendar", icon: Calendar },
  { id: "vllm", label: "vLLM Server", icon: Server },
  { id: "agent", label: "AI Agent", icon: Bot },
  { id: "formats", label: "Input/Output", icon: FileJson },
  { id: "submission", label: "Submission", icon: Trophy },
];

export const Sidebar = ({ isOpen, onClose, activeSection, onSectionChange }: SidebarProps) => {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 md:hidden" 
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside className={cn(
        "fixed top-14 sm:top-16 left-0 z-50 w-64 sm:w-72 h-[calc(100vh-3.5rem)] sm:h-[calc(100vh-4rem)] bg-card border-r border-border transform transition-transform duration-300",
        "md:sticky md:transform-none",
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}>
        <div className="flex items-center justify-between p-3 sm:p-4 border-b border-border md:hidden">
          <h2 className="font-semibold text-foreground text-sm sm:text-base">Navigation</h2>
          <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0">
            <X className="h-4 w-4" />
          </Button>
        </div>
        
        <ScrollArea className="h-full p-3 sm:p-4">
          <nav className="space-y-1 sm:space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeSection === item.id;
              
              return (
                <Button
                  key={item.id}
                  variant={isActive ? "secondary" : "ghost"}
                  className={cn(
                    "w-full justify-start text-left h-auto py-2 sm:py-3 px-2 sm:px-3",
                    isActive && "bg-accent/10 border border-accent/20"
                  )}
                  onClick={() => {
                    onSectionChange(item.id);
                    onClose();
                  }}
                >
                  <Icon className={cn(
                    "h-4 w-4 mr-2 sm:mr-3 flex-shrink-0",
                    isActive ? "text-accent" : "text-muted-foreground"
                  )} />
                  <span className={cn(
                    "text-xs sm:text-sm truncate",
                    isActive ? "text-foreground font-medium" : "text-muted-foreground"
                  )}>
                    {item.label}
                  </span>
                  {isActive && (
                    <ChevronRight className="h-3 w-3 sm:h-4 sm:w-4 ml-auto text-accent flex-shrink-0" />
                  )}
                </Button>
              );
            })}
          </nav>
        </ScrollArea>
      </aside>
    </>
  );
};