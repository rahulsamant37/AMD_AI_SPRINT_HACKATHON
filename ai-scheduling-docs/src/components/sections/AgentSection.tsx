import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CodeBlock } from "../CodeBlock";
import { Bot, ExternalLink, Brain, MessageSquare, Code, Info, Workflow } from "lucide-react";

export const AgentSection = () => {
  const agentCode = `import json
import openai

# We defined the base URL for our DeepSeek server
BASE_URL = "http://localhost:3000/v1"

class AI_AGENT:
    def __init__(self, client, MODEL_PATH):
        self.base_url = BASE_URL
        self.model_path = MODEL_PATH

    def parse_email(self, email_text):
        # We sent a request to our model with a carefully engineered prompt
        response = client.chat.completions.create(
            model=self.model_path,
            temperature=0.0, # We set temperature to 0.0 for deterministic output
            messages=[{
                "role": "user",
                "content": f"""
                You are an Agent that helps in scheduling meetings.
                Your job is to extract Email ID's and Meeting Duration.
                Return as json with 'participants', 'time_constraints' & 'meeting_duration'.
                Strictly follow the instructions. Strictly return dict with 
                participants email id's, time constraints & meeting duration in minutes only.
                Email: {email_text}
                """
            }]
        )
        # We loaded the response as a JSON object
        return json.loads(response.choices[0].message.content)

# How we used our agent
client = openai.OpenAI(
    base_url=BASE_URL,
    api_key="dummy" # A placeholder key was sufficient
)

agent = AI_AGENT(client, "/home/user/Models/deepseek-ai/deepseek-llm-7b-chat")

# Here's how we tested our agent's parsing ability
email_content = """
Hi team, let's meet on Thursday for 30 minutes to discuss 
the status of Agentic AI Project with John and Sarah.
"""

result = agent.parse_email(email_content)
print(json.dumps(result, indent=2))`;

  const setupSteps = `# Step 1: We started our vLLM Server with this command
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat \\
    --port 3000 ...`;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
          How We Built Our AI Agent with LangGraph
        </h2>
        <p className="text-muted-foreground text-lg">
          We built an intelligent agent that could autonomously parse requests and make scheduling decisions by orchestrating its logic within a robust LangGraph workflow.
        </p>
      </div>

      {/* Prerequisites */}
      <Alert>
        <Info className="h-4 w-4" />
        <AlertDescription>
          <strong>Prerequisite:</strong> Before building the agent, we first ensured our vLLM server was up and running with the DeepSeek model.
        </AlertDescription>
      </Alert>

      {/* Agent Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <Workflow className="h-5 w-5 text-accent" />
            </div>
            Our AI Agent's Architecture
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">
            Our AI Agent served as the core intelligent layer of our system. By using **LangGraph**, we structured its operations into a clear, stateful workflow. This allowed it to process natural language, interact with our LLMs, and convert unstructured requests into the structured data needed for scheduling.
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <MessageSquare className="h-8 w-8 mx-auto mb-3 text-accent" />
              <h4 className="font-semibold mb-2">Input Processing</h4>
              <p className="text-sm text-muted-foreground">We designed it to parse natural language emails.</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <Brain className="h-8 w-8 mx-auto mb-3 text-ai-blue" />
              <h4 className="font-semibold mb-2">Intelligence Layer</h4>
              <p className="text-sm text-muted-foreground">It extracted participants, duration, and other constraints.</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <Code className="h-8 w-8 mx-auto mb-3 text-ai-purple" />
              <h4 className="font-semibold mb-2">Output Generation</h4>
              <p className="text-sm text-muted-foreground">It generated structured JSON responses for our system.</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Setup Steps */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-secondary/10">
              <Code className="h-5 w-5 text-ai-blue" />
            </div>
            How We Built It
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center font-bold text-accent">
                1
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Started the vLLM Server</h4>
                <p className="text-muted-foreground mb-3">
                  First, we got our vLLM server running with the DeepSeek model using this command.
                </p>
                <CodeBlock language="bash" title="The Terminal Command We Used">
                  {setupSteps}
                </CodeBlock>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center font-bold text-accent">
                2
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Built the LangGraph Workflow</h4>
                <p className="text-muted-foreground">
                  We then defined the agent's logic as a stateful graph, orchestrating calls to the LLM for each step of the process.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center font-bold text-accent">
                3
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Tested and Iterated</h4>
                <p className="text-muted-foreground">
                  We tested our agent with different email formats and refined our prompts and workflow logic to achieve better accuracy.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Sample Implementation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-accent/10">
              <Brain className="h-5 w-5 text-ai-cyan" />
            </div>
            Our AI Agent Implementation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-4">
            Here's the Python code for the AI Agent we built to parse email content and extract meeting information:
          </p>
          
          <CodeBlock language="python" title="ai_agent.py">
            {agentCode}
          </CodeBlock>
        </CardContent>
      </Card>

      {/* Agent Capabilities */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <MessageSquare className="h-5 w-5 text-accent" />
            </div>
            What Our Agent Accomplished
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Email Processing</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  It successfully extracted participant email addresses.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  It accurately parsed meeting durations from text.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  It correctly identified time constraints and preferences.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  We implemented logic to handle name-to-email conversion.
                </li>
              </ul>
            </div>
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Output Format</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  We ensured it produced structured JSON responses.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  We standardized all field names for consistency.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  We included error handling and validation logic.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  We maintained consistent data types in the output.
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Best Practices */}
      <Card className="border-accent/20 bg-gradient-primary/5">
        <CardHeader>
          <CardTitle>Best Practices We Followed</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <Badge className="bg-accent/10 text-accent border-accent/20">Prompt Engineering</Badge>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• We were specific about our desired output format.</li>
                <li>• We provided the model with clear examples.</li>
                <li>• We used structured instructions in our prompts.</li>
                <li>• We made sure to handle edge cases explicitly.</li>
              </ul>
            </div>
            <div className="space-y-3">
              <Badge className="bg-ai-blue/10 text-ai-blue border-ai-blue/20">Error Handling</Badge>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• We always validated the JSON responses.</li>
                <li>• We set temperature to 0.0 for consistent results.</li>
                <li>• We implemented retry mechanisms for reliability.</li>
                <li>• We logged any failed parsing attempts for debugging.</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notebook Link */}
      <Card className="bg-gradient-secondary/5 border-ai-blue/20">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-semibold text-foreground mb-2">
                See Our Complete AI Agent
              </h4>
              <p className="text-muted-foreground">
                We've detailed our full implementation in the Sample AI Agent notebook.
              </p>
            </div>
            <Button className="bg-gradient-secondary hover:opacity-90" asChild>
              <a 
                href="https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Sample_AI_Agent.ipynb" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-2"
              >
                <ExternalLink className="h-4 w-4" />
                View Our Notebook
              </a>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};