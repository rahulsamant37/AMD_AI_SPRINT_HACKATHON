// src/pages/Index.tsx

import { useState } from "react";
import { Header } from "@/components/Header";
import { Sidebar } from "@/components/Sidebar";
import { IntroductionSection } from "@/components/sections/IntroductionSection";
import { SetupSection } from "@/components/sections/SetupSection";
import { CalendarSection } from "@/components/sections/CalendarSection";
import { VLLMSection } from "@/components/sections/VLLMSection";
import { AgentSection } from "@/components/sections/AgentSection";
import { FormatsSection } from "@/components/sections/FormatsSection";
import { SubmissionSection } from "@/components/sections/SubmissionSection";
import { ArchitectureSection } from "@/components/sections/ArchitectureSection";

// A map to make rendering sections cleaner and more declarative
const sections: { [key: string]: React.FC } = {
  introduction: IntroductionSection,
  setup: SetupSection,
  calendar: CalendarSection,
  vllm: VLLMSection,
  agent: AgentSection,
  formats: FormatsSection,
  architecture: ArchitectureSection,
  submission: SubmissionSection,
};

const Index = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true); // Default to open on desktop
  const [activeSection, setActiveSection] = useState("introduction");

  const handleOpenSidebar = () => setSidebarOpen(true);
  const handleCloseSidebar = () => setSidebarOpen(false);

  // Get the component to render based on the active section
  const ActiveSectionComponent = sections[activeSection] || IntroductionSection;

  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      {/* Header is now part of the main layout, ensuring it's always visible */}
      <Header onMenuToggle={handleOpenSidebar} />
      
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar now correctly handles opening, closing, and section changes */}
        <Sidebar
          isOpen={sidebarOpen}
          onClose={handleCloseSidebar}
          onOpen={handleOpenSidebar}
          activeSection={activeSection}
          onSectionChange={setActiveSection}
        />
        
        {/* Main content area with its own scrolling */}
        <main className="flex-1 w-full min-w-0 overflow-y-auto">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
            <div className="animate-fade-in">
              <ActiveSectionComponent />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Index;