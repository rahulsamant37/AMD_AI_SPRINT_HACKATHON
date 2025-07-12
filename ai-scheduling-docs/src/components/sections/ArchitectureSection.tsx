// src/components/sections/ArchitectureSection.tsx

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Network,
  Workflow,
  Puzzle,
  BarChart,
} from "lucide-react";

export const ArchitectureSection = () => {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
          Our System Architecture
        </h2>
        <p className="text-muted-foreground text-lg">
          Here’s a deep dive into how we designed and built our AI Scheduling Assistant from the ground up, using a multi-model architecture, a LangGraph workflow, and a comprehensive evaluation framework.
        </p>
      </div>

      {/* High-Level Architecture */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <Network className="h-5 w-5 text-accent" />
            </div>
            Our High-Level System Architecture
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">
            At the core of our project, we established a powerful infrastructure on the AMD MI300X GPU. We deployed three distinct vLLM servers to host our selected LLMs. This multi-model foundation allowed our AI Scheduling System to dynamically choose the best model for each task, orchestrated by our main application.
          </p>
          <div className="p-4 border rounded-xl bg-background/50 flex justify-center">
            <img 
              src="/diagrams/high-level-architecture.png" 
              alt="High-Level System Architecture Diagram" 
              className="w-full h-auto bg-white rounded-md p-2"
            />
          </div>
        </CardContent>
      </Card>

      {/* LangGraph Workflow */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-secondary/10">
              <Workflow className="h-5 w-5 text-ai-blue" />
            </div>
            How We Designed Our LangGraph Workflow
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">
            We used LangGraph to build a state machine that defined the precise, step-by-step logic our agent followed. This approach made our agent’s reasoning structured, observable, and easy to maintain. The workflow began with parsing the request and concluded by generating a complete, validated scheduling solution.
          </p>
          <div className="p-4 border rounded-xl bg-background/50 flex justify-center">
            <img 
              src="/diagrams/langgraph-workflow.png" 
              alt="LangGraph Workflow Diagram" 
              className="w-full h-auto bg-white rounded-md p-2"
            />
          </div>
        </CardContent>
      </Card>

      {/* Multi-Model Architecture */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-accent/10">
              <Puzzle className="h-5 w-5 text-ai-cyan" />
            </div>
            Our Multi-Model Evaluation Framework
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">
            A key part of our strategy was not to depend on a single LLM. We created a robust evaluation system to test our three models across six challenging scenarios. Based on the results, our system dynamically selected the top-performing DeepSeek 7B model, while keeping the other models available as reliable fallbacks.
          </p>
          <div className="p-4 border rounded-xl bg-background/50 flex justify-center">
            <img 
              src="/diagrams/multi-model-framework.png" 
              alt="Multi-Model Framework Diagram" 
              className="w-full h-auto bg-white rounded-md p-2"
            />
          </div>
        </CardContent>
      </Card>

      {/* Evaluation Framework */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <BarChart className="h-5 w-5 text-accent" />
            </div>
            The Evaluation Metrics We Used
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">
            To ensure our model selection was data-driven, we defined a clear set of metrics. We weighted correctness most heavily (40%), followed by latency (30%), conflict resolution (20%), and user preference adherence (10%). This framework allowed us to objectively rank our models and select the best one for the job.
          </p>
          <div className="p-4 border rounded-xl bg-background/50 flex justify-center">
            <img 
              src="/diagrams/evaluation-metrics.png" 
              alt="Evaluation Metrics Diagram"
              className="w-full h-auto bg-white rounded-md p-2"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};