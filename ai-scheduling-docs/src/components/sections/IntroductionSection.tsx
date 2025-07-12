import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FeatureCard } from "../FeatureCard";
import { 
  Bot, 
  Brain, 
  Calendar, 
  Zap, 
  Target, 
  Users, 
  MessageSquare,
  Globe
} from "lucide-react";
import heroImage from "@/assets/hero-ai-scheduling.jpg";

export const IntroductionSection = () => {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-xl sm:rounded-2xl bg-gradient-primary/10 border border-accent/20">
        <div className="absolute inset-0">
          <img 
            src={heroImage} 
            alt="AI Scheduling Assistant"
            className="w-full h-full object-cover opacity-20"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-background/80 to-background/40" />
        </div>
        <div className="relative z-10 p-6">
          <div className="max-w-4xl">
            <Badge className="mb-3 sm:mb-4 bg-accent/10 text-accent border-accent/20 text-xs sm:text-sm">
              AMD AI Hackathon 2025
            </Badge>
            <h1 className="text-3xl sm:text-4xl lg:text-6xl font-bold mb-4 sm:mb-6 leading-tight">
              <span className="bg-gradient-primary bg-clip-text text-transparent">
                Our Agentic AI
              </span>
              <br />
              Scheduling Assistant
            </h1>
            <p className="text-base sm:text-lg lg:text-xl text-muted-foreground mb-6 sm:mb-8 leading-relaxed max-w-3xl">
              We built an intelligent scheduling system that leverages Agentic AI to autonomously 
              coordinate meetings, resolve conflicts, and optimize calendars—all without human intervention.
            </p>
            <div className="flex flex-wrap gap-2 sm:gap-3">
              <Badge variant="secondary" className="text-xs sm:text-sm py-1 px-2 sm:px-3">
                🤖 Autonomous AI
              </Badge>
              <Badge variant="secondary" className="text-xs sm:text-sm py-1 px-2 sm:px-3">
                📅 Calendar Integration
              </Badge>
              <Badge variant="secondary" className="text-xs sm:text-sm py-1 px-2 sm:px-3">
                🚀 vLLM Server
              </Badge>
              <Badge variant="secondary" className="text-xs sm:text-sm py-1 px-2 sm:px-3">
                ⚡ AMD MI300X GPU
              </Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <Bot className="h-5 w-5 text-accent" />
            </div>
            Project Overview
          </CardTitle>
        </CardHeader>
        <CardContent className="prose prose-invert max-w-none">
          <p className="text-muted-foreground leading-relaxed">
            <strong>Event:</strong> AMD AI Sprint — Agentic AI Scheduling Assistant Hackathon  <br />
            <strong>Venue:</strong> IIT Bombay, Mumbai | <strong>Date:</strong> July 12–13, 2025  
          </p>
          <p className="text-muted-foreground leading-relaxed mt-2">
            <strong>The Challenge:</strong> At this high-level hackathon, we focused on building autonomous AI agents using AMD’s MI300X GPUs. Our goal was to design a smart scheduling assistant that could intelligently coordinate meetings across different people and time zones.
          </p>
          <p className="text-muted-foreground leading-relaxed mt-2">
            <strong>Our Contribution:</strong> We developed an Agentic AI Assistant that autonomously schedules and reschedules meetings. It works by scanning calendars, resolving conflicts between participants, and proposing the best time slots, which completely removes the usual back-and-forth from scheduling.
          </p>
        </CardContent>
      </Card>

      {/* Why We Chose Agentic AI */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-secondary/10">
              <Brain className="h-5 w-5 text-ai-purple" />
            </div>
            Why We Chose Agentic AI
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">
            While traditional tools depend on basic rules or manual input, our solution goes much further. 
            Here’s what our Agentic AI does differently:
          </p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <FeatureCard
              icon={Brain}
              title="Human-like Reasoning"
              description="Our AI prioritizes attendees, resolves scheduling conflicts, and makes intelligent decisions on its own."
            />
            <FeatureCard
              icon={Zap}
              title="Independent Action"
              description="It independently sends follow-ups, adjusts for time zones, and proactively handles complex scheduling cases."
            />
            <FeatureCard
              icon={Target}
              title="Learned Preferences"
              description="We designed it to learn and adapt to user behaviors, preferred meeting times, and recurring patterns."
            />
          </div>
        </CardContent>
      </Card>

      {/* Key Features We Implemented */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-accent/10">
              <Calendar className="h-5 w-5 text-ai-cyan" />
            </div>
            Key Features We Implemented
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-2 gap-4 sm:gap-6">
            <div className="space-y-3 sm:space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center mt-1">
                  <div className="w-2 h-2 rounded-full bg-accent" />
                </div>
                <div>
                  <h4 className="font-semibold text-foreground">Autonomous Coordination</h4>
                  <p className="text-sm text-muted-foreground">We made sure the AI initiates all scheduling without needing human micromanagement.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center mt-1">
                  <div className="w-2 h-2 rounded-full bg-accent" />
                </div>
                <div>
                  <h4 className="font-semibold text-foreground">Dynamic Adaptability</h4>
                  <p className="text-sm text-muted-foreground">Our assistant was built to handle last-minute changes and conflicting priorities smoothly.</p>
                </div>
              </div>
            </div>
            <div className="space-y-3 sm:space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center mt-1">
                  <div className="w-2 h-2 rounded-full bg-accent" />
                </div>
                <div>
                  <h4 className="font-semibold text-foreground">Natural Language Interaction</h4>
                  <p className="text-sm text-muted-foreground">We implemented a conversational interface so users can just talk to the AI.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center mt-1">
                  <div className="w-2 h-2 rounded-full bg-accent" />
                </div>
                <div>
                  <h4 className="font-semibold text-foreground">Live Calendar Integration</h4>
                  <p className="text-sm text-muted-foreground">We synced it with Google Calendar to ensure all coordination happens in real-time.</p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* How We Measured Success */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <Target className="h-5 w-5 text-accent" />
            </div>
            How We Measured Success
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">Our final solution excels in the following areas:</p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <FeatureCard
              icon={Bot}
              title="Autonomy"
              description="We achieved minimal human intervention, even for the most complex scheduling tasks."
            />
            <FeatureCard
              icon={Target}
              title="Accuracy"
              description="Our system produced very few errors or conflicts and demonstrated optimal time allocation."
            />
            <FeatureCard
              icon={Users}
              title="User Experience"
              description="We designed an intuitive interface that actively saves users time and reduces scheduling friction."
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};