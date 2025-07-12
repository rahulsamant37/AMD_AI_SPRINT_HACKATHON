// src/components/Sidebar.tsx

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
  ChevronRight,
  ServerCog,
  PanelLeftClose,
  PanelRightOpen,
} from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onOpen: () => void;
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
  { id: "architecture", label: "Architecture", icon: ServerCog },
  { id: "submission", label: "Submission", icon: Trophy },
];

export const Sidebar = ({ 
  isOpen, 
  onClose, 
  onOpen, 
  activeSection, 
  onSectionChange 
}: SidebarProps) => {
  return (
    <>
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 md:hidden" 
          onClick={onClose}
        />
      )}
      
      <aside className={cn(
        "fixed md:sticky top-0 z-50 h-screen bg-card border-r border-border transition-all duration-300 flex flex-col",
        isOpen ? "translate-x-0" : "-translate-x-full",
        "md:translate-x-0", 
        isOpen ? "w-64 sm:w-72" : "w-0 md:w-16" 
      )}>
        <div className={cn(
            "h-full flex flex-col w-full overflow-hidden",
            isOpen ? "opacity-100" : "opacity-0 md:opacity-100"
        )}>
            <div className="flex items-center justify-between p-3 sm:p-4 border-b border-border md:hidden">
              <h2 className="font-semibold text-foreground text-sm sm:text-base">Navigation</h2>
              <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0">
                <X className="h-4 w-4" />
              </Button>
            </div>
        
            {/* Main Navigation */}
            <ScrollArea className="flex-1 md:mt-0 p-3 sm:p-4" style={{position:'relative'}}>
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
                        if (window.innerWidth < 768) {
                          onClose();
                        }
                      }}
                    >
                      <Icon style={{marginLeft:'-5px'}} className={cn(
                        "h-4 w-4 mr-2 sm:mr-3 flex-shrink-0",
                        isActive ? "text-accent" : "text-muted-foreground"
                      )} />
                      <span className={cn(
                        "text-xs sm:text-sm truncate",
                        "transition-opacity duration-100",
                        isOpen ? "opacity-100" : "opacity-0 md:opacity-100",
                        !isOpen && "md:hidden" 
                      )}>
                        {item.label}
                      </span>
                      {isActive && isOpen && (
                        <ChevronRight className="h-3 w-3 sm:h-4 sm:w-4 ml-auto text-accent flex-shrink-0" />
                      )}
                    </Button>
                    
                  );
                })}
              </nav>
                          <div className="hidden md:block absolute right-4 z-50" style={{bottom:'80px'}}>
                <Button variant="ghost" size="icon" onClick={onClose} className={cn("h-8 w-8", !isOpen && "md:hidden")}>
                    <PanelLeftClose className="h-4 w-4 text-muted-foreground" />
                    <span className="sr-only">Collapse Sidebar</span>
                </Button>
            </div>
            </ScrollArea>
        </div>
      </aside>

      {!isOpen && (
        <div className="hidden md:block fixed bottom-4 left-4 z-50">
            <Button variant="outline" size="icon" onClick={onOpen}>
                <PanelRightOpen className="h-5 w-5" />
                <span className="sr-only">Open Sidebar</span>
            </Button>
        </div>
      )}
    </>
  );
};