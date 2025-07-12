import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CodeBlock } from "../CodeBlock";
import { FileJson, ArrowRight, AlertTriangle, CheckCircle2, ExternalLink } from "lucide-react";
import { Button } from "../ui/button";

export const FormatsSection = () => {
  const inputJson = `{
    "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
    "Datetime": "09-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "userone.amd@gmail.com",
    "Attendees": [
        {
            "email": "usertwo.amd@gmail.com"
        },
        {
            "email": "userthree.amd@gmail.com"
        }
    ],
    "Subject": "Agentic AI Project Status Update",
    "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project."
}`;

  const processedJson = `{
    "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
    "Datetime": "09-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "userone.amd@gmail.com",
    "Attendees": [
        {
            "email": "usertwo.amd@gmail.com"
        },
        {
            "email": "userthree.amd@gmail.com"
        }
    ],
    "Subject": "Agentic AI Project Status Update",
    "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project.",
    "Start": "2025-07-17T00:00:00+05:30",
    "End": "2025-07-17T23:59:59+05:30",
    "Duration_mins": "30"
}`;

  const finalOutputJson = `{
    "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
    "Datetime": "09-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "userone.amd@gmail.com",
    "Attendees": [
        {
            "email": "userone.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:30:00+05:30",
                    "EndTime": "2025-07-17T11:00:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Agentic AI Project Status Update"
                }
            ]
        },
        {
            "email": "usertwo.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:00:00+05:30",
                    "EndTime": "2025-07-17T10:30:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Team Meet"
                },
                {
                    "StartTime": "2025-07-17T10:30:00+05:30",
                    "EndTime": "2025-07-17T11:00:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Agentic AI Project Status Update"
                }
            ]
        },
        {
            "email": "userthree.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:00:00+05:30",
                    "EndTime": "2025-07-17T10:30:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Team Meet"
                },
                {
                    "StartTime": "2025-07-17T13:00:00+05:30",
                    "EndTime": "2025-07-17T14:00:00+05:30",
                    "NumAttendees": 1,
                    "Attendees": [
                        "SELF"
                    ],
                    "Summary": "Lunch with Customers"
                },
                {
                    "StartTime": "2025-07-17T10:30:00+05:30",
                    "EndTime": "2025-07-17T11:00:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Agentic AI Project Status Update"
                }
            ]
        }
    ],
    "Subject": "Agentic AI Project Status Update",
    "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project.",
    "EventStart": "2025-07-17T10:30:00+05:30",
    "EventEnd": "2025-07-17T11:00:00+05:30",
    "Duration_mins": "30"
}`;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
          Our Input & Output Formats
        </h2>
        <p className="text-muted-foreground text-lg">
          Here’s how we structured the JSON data to process our scheduling requests from start to finish.
        </p>
      </div>

      {/* Format Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <FileJson className="h-5 w-5 text-accent" />
            </div>
            Our Data Flow
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center gap-8 py-6">
            <div className="text-center" style={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
              <div className="w-16 h-16 rounded-full bg-accent/10 border-2 border-accent/20 flex items-center justify-center mb-3">
                <FileJson className="h-8 w-8 text-accent" />
              </div>
              <h4 className="font-semibold text-foreground">Input JSON</h4>
              <p className="text-sm text-muted-foreground">This was our raw meeting request.</p>
            </div>
            
            <ArrowRight className="h-6 w-6 text-muted-foreground" />
            
            <div className="text-center" style={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
              <div className="w-16 h-16 rounded-full bg-ai-blue/10 border-2 border-ai-blue/20 flex items-center justify-center mb-3">
                <FileJson className="h-8 w-8 text-ai-blue" />
              </div>
              <h4 className="font-semibold text-foreground">Processed JSON</h4>
              <p className="text-sm text-muted-foreground">We enhanced it with our AI.</p>
            </div>
            
            <ArrowRight className="h-6 w-6 text-muted-foreground" />
            
            <div className="text-center" style={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
              <div className="w-16 h-16 rounded-full bg-ai-cyan/10 border-2 border-ai-cyan/20 flex items-center justify-center mb-3">
                <FileJson className="h-8 w-8 text-ai-cyan" />
              </div>
              <h4 className="font-semibold text-foreground">Final Output</h4>
              <p className="text-sm text-muted-foreground">This was our final, complete schedule.</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* JSON Formats */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-secondary/10">
              <FileJson className="h-5 w-5 text-ai-blue" />
            </div>
            How We Defined Our JSON Formats
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="input" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="input">Our Input JSON</TabsTrigger>
              <TabsTrigger value="processed">Our Processed JSON</TabsTrigger>
              <TabsTrigger value="output">Our Final Output</TabsTrigger>
            </TabsList>
            <br />
            
            <TabsContent value="input" className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Badge className="bg-accent/10 text-accent border-accent/20">
                    Input Format
                  </Badge>
                  <p className="text-muted-foreground">This was the initial data structure we started with.</p>
                </div>
                
                <CodeBlock language="json" title="input_request.json">
                  {inputJson}
                </CodeBlock>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <h4 className="font-semibold text-foreground">The Required Fields We Used:</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• <code className="text-accent">Request_id</code> - A unique ID we assigned.</li>
                      <li>• <code className="text-accent">From</code> - The email of the meeting organizer.</li>
                      <li>• <code className="text-accent">Attendees</code> - An array of all participant objects.</li>
                      <li>• <code className="text-accent">Subject</code> - The title of the meeting.</li>
                      <li>• <code className="text-accent">EmailContent</code> - The original email text we processed.</li>
                    </ul>
                  </div>
                  <div className="space-y-3">
                    <h4 className="font-semibold text-foreground">The Metadata Fields We Included:</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• <code className="text-ai-cyan">Datetime</code> - The timestamp of the request.</li>
                      <li>• <code className="text-ai-cyan">Location</code> - The location context for the meeting.</li>
                    </ul>
                  </div>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="processed" className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Badge className="bg-ai-blue/10 text-ai-blue border-ai-blue/20">
                    Processed Format
                  </Badge>
                  <p className="text-muted-foreground">Here’s how we structured the data after our AI enhanced it.</p>
                </div>
                
                <Alert>
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Note on Evaluation:</strong> We understood this output format would be evaluated for our qualification and final score.
                  </AlertDescription>
                </Alert>

                <CodeBlock language="json" title="processed_request.json">
                  {processedJson}
                </CodeBlock>

                <div className="space-y-3">
                  <h4 className="font-semibold text-foreground">New Fields Our AI Added:</h4>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• <code className="text-accent">Start</code> - The start time boundary we extracted.</li>
                    <li>• <code className="text-accent">End</code> - The end time boundary we extracted.</li>
                    <li>• <code className="text-accent">Duration_mins</code> - The meeting duration in minutes we parsed.</li>
                  </ul>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="output" className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Badge className="bg-ai-cyan/10 text-ai-cyan border-ai-cyan/20">
                    Final Output
                  </Badge>
                  <p className="text-muted-foreground">This was our complete solution, with calendar events integrated.</p>
                </div>
                
                <Alert>
                  <CheckCircle2 className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Submission Format:</strong> This was the final output format we submitted for the hackathon.
                  </AlertDescription>
                </Alert>

                <CodeBlock language="json" title="final_output.json">
                  {finalOutputJson}
                </CodeBlock>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <h4 className="font-semibold text-foreground">How We Integrated Calendars:</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• We included event listings for each attendee.</li>
                      <li>• We pulled in all existing calendar events.</li>
                      <li>• We applied our own conflict resolution logic.</li>
                      <li>• We selected the optimal time slot for the meeting.</li>
                    </ul>
                  </div>
                  <div className="space-y-3">
                    <h4 className="font-semibold text-foreground">The Event Details We Generated:</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• <code className="text-accent">StartTime</code> / <code className="text-accent">EndTime</code> - We used ISO format with timezones.</li>
                      <li>• <code className="text-accent">NumAttendees</code> - We calculated the count of participants.</li>
                      <li>• <code className="text-accent">Attendees</code> - We provided a list of emails or marked it as "SELF".</li>
                      <li>• <code className="text-accent">Summary</code> - We used the original event description.</li>
                    </ul>
                  </div>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Key Requirements */}
      <Card className="border-accent/20 bg-gradient-primary/5">
        <CardHeader>
          <CardTitle>How We Met the Key Requirements</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <Badge className="bg-accent/10 text-accent border-accent/20">Our Data Processing</Badge>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• We successfully extracted the meeting duration from natural language.</li>
                <li>• We parsed all time constraints and user preferences.</li>
                <li>• We identified every participant and converted their names to emails.</li>
                <li>• We maintained data integrity throughout our entire process.</li>
              </ul>
            </div>
            <div className="space-y-4">
              <Badge className="bg-ai-cyan/10 text-ai-cyan border-ai-cyan/20">Our Calendar Logic</Badge>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• We integrated existing calendar events for all attendees.</li>
                <li>• We found the optimal meeting slots and avoided conflicts.</li>
                <li>• We respected timezone information, using IST (+05:30).</li>
                <li>• We generated a complete and accurate final schedule output.</li>
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
                See Our Complete Input Output Formats
              </h4>
              <p className="text-muted-foreground">
                We've detailed our full implementation in the Sample Input Output Formats notebook.
              </p>
            </div>
            <Button className="bg-gradient-secondary hover:opacity-90" asChild>
              <a 
                href="https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Input_Output_Formats.ipynb" 
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