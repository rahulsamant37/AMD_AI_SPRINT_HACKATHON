import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CodeBlock } from "../CodeBlock";
import { Calendar, ExternalLink, Key, Database, Code, Info } from "lucide-react";

export const CalendarSection = () => {
  const sampleCode = `from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from datetime import datetime, timedelta

def get_calendar_events(user_email, start_date, end_date, token_file):
    """
    Retrieve Google Calendar events for a user within a date range.
    
    Args:
        user_email (str): Email of the calendar owner
        start_date (str): Start date in ISO format
        end_date (str): End date in ISO format
        token_file (str): Path to OAuth token file
    
    Returns:
        list: Processed calendar events
    """
    # Load credentials from token file
    creds = Credentials.from_authorized_user_file(token_file)
    
    # Build the Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    
    # Call the Calendar API
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_date,
        timeMax=end_date,
        maxResults=100,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Process events
    processed_events = []
    for event in events:
        processed_event = {
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'summary': event.get('summary', 'No Title'),
            'attendees': len(event.get('attendees', [])),
            'attendee_emails': [a.get('email') for a in event.get('attendees', [])]
        }
        processed_events.append(processed_event)
    
    return processed_events`;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
          How We Integrated Google Calendar
        </h2>
        <p className="text-muted-foreground text-lg">
          Here’s how we programmatically extracted and processed Google Calendar events for our AI.
        </p>
      </div>

      {/* Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <Calendar className="h-5 w-5 text-accent" />
            </div>
            Our Approach to Event Extraction
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">
            In our notebook, we demonstrated how we programmatically retrieved and processed Google Calendar 
            events for a given user. We used the Google Auth Tokens provided at the hackathon 
            to pull event data.
          </p>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Key Skills We Applied:</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  Authenticated with OAuth tokens
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  Made API calls to the Google Calendar service
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  Processed complex event data structures
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2" />
                  Extracted key attendee information
                </li>
              </ul>
            </div>
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">The Output We Generated:</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  A structured and organized event list
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  Attendee counts and their email addresses
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  Precise time slots and meeting durations
                </li>
                <li className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-ai-cyan mt-2" />
                  A clean, processable data format for our AI
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Key Steps */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-secondary/10">
              <Code className="h-5 w-5 text-ai-blue" />
            </div>
            The Steps We Took
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center font-bold text-accent">
                1
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Authentication</h4>
                <p className="text-muted-foreground">First, we loaded the user credentials from the provided token file using Google OAuth2.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center font-bold text-accent">
                2
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-2">API Call</h4>
                <p className="text-muted-foreground">Next, we fetched calendar events between specified start and end dates via the Google Calendar API.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center font-bold text-accent">
                3
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Data Processing</h4>
                <p className="text-muted-foreground">We then extracted all relevant event details and structured them into a clean, usable format.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center font-bold text-accent">
                4
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Final Output</h4>
                <p className="text-muted-foreground">Finally, our script returned a processed list of events, complete with attendee counts and time slots.</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Code Example */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-accent/10">
              <Database className="h-5 w-5 text-ai-cyan" />
            </div>
            Our Python Implementation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <CodeBlock language="python" title="calendar_extraction.py">
            {sampleCode}
          </CodeBlock>
        </CardContent>
      </Card>

      {/* Important Notes */}
      <Alert>
        <Info className="h-4 w-4" />
        <AlertDescription>
          <strong>Authentication Note:</strong> For this project, we utilized the pre-configured Google Auth Tokens 
          provided for the hackathon, which allowed us to access calendar data seamlessly during the event.
        </AlertDescription>
      </Alert>

      {/* Notebook Link */}
      <Card className="bg-gradient-primary/5 border-accent/20">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-semibold text-foreground mb-2">
                See Our Complete Implementation
              </h4>
              <p className="text-muted-foreground">
                We've detailed our full implementation in the Calendar Event Extraction notebook.
              </p>
            </div>
            <Button className="bg-gradient-primary hover:opacity-90" asChild>
              <a 
                href="https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Calendar_Event_Extraction.ipynb" 
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