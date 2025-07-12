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

const Index = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeSection, setActiveSection] = useState("introduction");

  const renderSection = () => {
    switch (activeSection) {
      case "introduction":
        return <IntroductionSection />;
      case "setup":
        return <SetupSection />;
      case "calendar":
        return <CalendarSection />;
      case "vllm":
        return <VLLMSection />;
      case "agent":
        return <AgentSection />;
      case "formats":
        return <FormatsSection />;
      case "submission":
        return <SubmissionSection />;
      default:
        return <IntroductionSection />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
      
      <div className="flex">
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          activeSection={activeSection}
          onSectionChange={setActiveSection}
        />
        
        <main className="flex-1 w-full min-w-0">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
            <div className="animate-fade-in">
              {renderSection()}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Index;
