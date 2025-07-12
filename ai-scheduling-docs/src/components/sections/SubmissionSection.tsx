import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CodeBlock } from "../CodeBlock";
import { Trophy, ExternalLink, Clock, Target, GitBranch, Lightbulb, AlertTriangle } from "lucide-react";

export const SubmissionSection = () => {
  const submissionCode = `def our_meeting_assistant(input_json):
    """
    Our AI Meeting Assistant Implementation
    
    Args:
        input_json (dict): Meeting request in the specified input format
        
    Returns:
        dict: Response with 'processed' and 'output' fields
    """
    # This is where we integrated all our components
    
    # Step 1: We parsed the input and extracted information using our AI agent
    processed_data = self.process_with_ai_agent(input_json)
    
    # Step 2: We then fetched the calendar events for all attendees
    calendar_events = self.get_calendar_events_for_attendees(
        attendees=processed_data['attendees'],
        start_date=processed_data['start'],
        end_date=processed_data['end']
    )
    
    # Step 3: Our logic then found the optimal meeting slot
    optimal_slot = self.find_optimal_meeting_slot(
        calendar_events=calendar_events,
        duration_mins=processed_data['duration_mins'],
        constraints=processed_data['time_constraints']
    )
    
    # Step 4: Finally, we generated the final output format
    final_output = self.generate_final_output(
        input_data=input_json,
        processed_data=processed_data,
        calendar_events=calendar_events,
        meeting_slot=optimal_slot
    )
    
    # We returned both the processed data and the final output as required
    return {
        "processed": processed_data,
        "output": final_output
    }

# This is how our code was executed for the final evaluation
if __name__ == "__main__":
    import json
    
    # We were tested with sample inputs like this one
    sample_input = {
        "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
        "Datetime": "09-07-2025T12:34:55",
        "Location": "IIT Mumbai",
        "From": "userone.amd@gmail.com",
        "Attendees": [
            {"email": "usertwo.amd@gmail.com"},
            {"email": "userthree.amd@gmail.com"}
        ],
        "Subject": "Agentic AI Project Status Update",
        "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project."
    }
    
    result = our_meeting_assistant(sample_input)
    print(json.dumps(result, indent=2))`;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
          Our Submission & Evaluation
        </h2>
        <p className="text-muted-foreground text-lg">
          Here’s how we finalized our implementation and prepared for the final evaluation.
        </p>
      </div>

      {/* Submission Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <Trophy className="h-5 w-5 text-accent" />
            </div>
            How We Submitted Our Project
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Alert className="mb-6">
            <Clock className="h-4 w-4" />
            <AlertDescription>
              <strong>The Deadline:</strong> We executed our final code at 2:00 PM on hackathon day. We had our server running on Port 5000, ready to receive test JSONs and return our AI Assistant's responses.
            </AlertDescription>
          </Alert>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Our Core Function</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  We implemented the <code className="text-accent">our_meeting_assistant()</code> function.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  It took a meeting request JSON as its input.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  It returned a dictionary with<code className="text-accent">processed</code> and <code className="text-accent">output</code> fields.
                </li>
              </ul>
            </div>
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Our Evaluation Setup</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  We had our server running on Port 5000.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  The evaluation was done through automated JSON testing.
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  We ensured strict format compliance for our output.
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Implementation Template */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-secondary/10">
              <Target className="h-5 w-5 text-ai-blue" />
            </div>
            The Final Implementation We Submitted
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-4">
            We followed this structure for our main submission function, bringing all our modules together.
          </p>
          
          <CodeBlock language="python" title="submission.py">
            {submissionCode}
          </CodeBlock>
        </CardContent>
      </Card>

      {/* Evaluation Criteria */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-accent/10">
              <Target className="h-5 w-5 text-ai-cyan" />
            </div>
            How Our Work Was Evaluated
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <Target className="h-8 w-8 mx-auto mb-3 text-accent" />
              <h4 className="font-semibold mb-2">Correctness</h4>
              <p className="text-sm text-muted-foreground">We were graded on the accuracy and precision of our results.</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <Clock className="h-8 w-8 mx-auto mb-3 text-ai-blue" />
              <h4 className="font-semibold mb-2">Latency</h4>
              <p className="text-sm text-muted-foreground">Our solution's speed and efficiency were measured.</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <GitBranch className="h-8 w-8 mx-auto mb-3 text-ai-purple" />
              <h4 className="font-semibold mb-2">Repository</h4>
              <p className="text-sm text-muted-foreground">Our code organization and documentation were assessed.</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <Lightbulb className="h-8 w-8 mx-auto mb-3 text-ai-cyan" />
              <h4 className="font-semibold mb-2">Creativity</h4>
              <p className="text-sm text-muted-foreground">The innovation and uniqueness of our approach were scored.</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50 md:col-span-2">
              <Trophy className="h-8 w-8 mx-auto mb-3 text-accent" />
              <h4 className="font-semibold mb-2">Overall Performance</h4>
              <p className="text-sm text-muted-foreground">All factors were combined to determine the best solution.</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Scoring Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle>The Detailed Scoring Metrics We Focused On</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <Badge className="bg-accent/10 text-accent border-accent/20 mt-1">
                35%
              </Badge>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Correctness of Our Output</h4>
                <p className="text-muted-foreground">
                  We focused on JSON format compliance, accurate time extraction, proper calendar integration, and solid conflict resolution.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <Badge className="bg-ai-blue/10 text-ai-blue border-ai-blue/20 mt-1">
                25%
              </Badge>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Our Roundtrip Latency</h4>
                <p className="text-muted-foreground">
                  We optimized our AI agent and calendar logic to ensure a fast response time from input to output.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <Badge className="bg-ai-purple/10 text-ai-purple border-ai-purple/20 mt-1">
                20%
              </Badge>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Our GitHub Repository Quality</h4>
                <p className="text-muted-foreground">
                  We maintained a clean project structure with good documentation, clear commit messages, and a complete README.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <Badge className="bg-ai-cyan/10 text-ai-cyan border-ai-cyan/20 mt-1">
                20%
              </Badge>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Our Creative Approach</h4>
                <p className="text-muted-foreground">
                  We aimed for innovation in our agent's design and used a unique approach to solve the scheduling problem.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Final Checklist */}
      <Card className="border-accent/20 bg-gradient-primary/5">
        <CardHeader>
          <CardTitle>Our Pre-Submission Checklist</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <Badge className="bg-accent/10 text-accent border-accent/20">Technical Requirements We Met</Badge>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>✓ We implemented the <code className="text-accent">our_meeting_assistant()</code> function.</li>
                <li>✓ Our function returned a dict with <code className="text-accent">processed</code> and <code className="text-accent">output</code> fields.</li>
                <li>✓ Our output strictly followed the specified JSON format.</li>
                <li>✓ Our server was ready to accept connections on Port 5000.</li>
                <li>✓ We installed and configured all dependencies.</li>
              </ul>
            </div>
            <div className="space-y-3">
              <Badge className="bg-ai-blue/10 text-ai-blue border-ai-blue/20">Quality Assurance We Performed</Badge>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>✓ We tested our code with multiple sample inputs.</li>
                <li>✓ We implemented robust error handling.</li>
                <li>✓ We organized and documented our GitHub repository.</li>
                <li>✓ We confirmed our vLLM server and AI agent were working correctly.</li>
                <li>✓ We verified our calendar integration was fully functional.</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notebook Link */}
      <Card className="bg-gradient-accent/5 border-ai-cyan/20">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-semibold text-foreground mb-2">
                See Our Complete Submission
              </h4>
              <p className="text-muted-foreground">
                We followed the detailed submission notebook for our final implementation.
              </p>
            </div>
            <Button className="bg-gradient-accent hover:opacity-90" asChild>
              <a 
                href="https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Submission.ipynb" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-2"
              >
                <ExternalLink className="h-4 w-4" />
                View Our Submission Notebook
              </a>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Final Warning */}
      <Alert>
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>
          <strong>A Critical Point We Adhered To:</strong> We knew that our output had to strictly follow the specified format. Any deviation would lead to failure, so we tested our solution thoroughly before the final deadline.
        </AlertDescription>
      </Alert>
    </div>
  );
};