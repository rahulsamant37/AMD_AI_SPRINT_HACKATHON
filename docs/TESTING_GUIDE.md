# SchedulAI - Complete Testing Guide

## 🚀 **Application Startup Steps**

### **Step 1: Environment Setup**

1. **Activate Virtual Environment**
   ```bash
   cd SchedulAI
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Verify Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check Configuration**
   ```bash
   # Ensure .env file exists with required variables
   cat .env
   
   # Required variables:
   # VLLM_BASE_URL=http://localhost:3000
   # VLLM_MODEL_PATH=/home/user/Models/deepseek-ai/deepseek-llm-7b-chat
   # GOOGLE_CREDENTIALS_FILE=credentials.json
   ```

4. **Verify Google Credentials**
   ```bash
   # Check if credentials.json exists
   ls -la credentials.json
   
   # Check if token.pickle exists (created after first OAuth)
   ls -la token.pickle
   ```

### **Step 2: Start the Application**

**Method 1: Direct Module Execution (Recommended)**
```bash
python -m app.main
```

**Method 2: Using Uvicorn**
```bash
uvicorn app.main:app --host localhost --port 5000 --reload
```

**Expected Startup Output:**
```
2025-01-05 10:00:00 - scheduleai - INFO - Logging configured for scheduleai - Level: INFO
2025-01-05 10:00:00 - scheduleai - INFO - Creating SchedulAI FastAPI application...
2025-01-05 10:00:00 - scheduleai - INFO - SchedulAI application created successfully
2025-01-05 10:00:00 - scheduleai - INFO - Starting SchedulAI FastAPI Server...
2025-01-05 10:00:00 - scheduleai - INFO - Configuration validated successfully
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:5000 (Press CTRL+C to quit)
```

---

## 🧪 **Comprehensive Testing Steps**

### **Test 1: System Health Check**

**Objective**: Verify all core services are operational

```bash
curl http://localhost:5000/health | python -m json.tool
```

**Expected Response:**
```json
{
  "status": "healthy",
  "services": {
    "google_calendar": true,
    "gmail_api": true,
    "vllm_agent": true,
    "function_calling": true
  },
  "agent_tools_count": 5,
  "config": {
    "debug_mode": true,
    "log_level": "INFO"
  },
  "timestamp": "2025-01-05T10:00:00.000000",
  "error": null
}
```

**✅ Success Criteria:**
- Status: "healthy"
- All services: true
- Agent tools count: 5
- No errors

---

### **Test 2: API Overview**

**Objective**: Verify API is accessible and shows correct information

```bash
curl http://localhost:5000/ | python -m json.tool
```

**Expected Response:**
```json
{
  "message": "SchedulAI API",
  "version": "1.0.0",
  "features": [
    "vLLM DeepSeek Integration",
    "Google Calendar & Gmail",
    "Autonomous Scheduling"
  ],
  "status": "active",
  "architecture": "Layered Architecture with Domain Separation",
  "endpoints": {
    "health": "/health",
    "schedule": "/meetings/schedule",
    "proposals": "/meetings/proposal/{proposal_id}",
    "confirm": "/meetings/confirm/{proposal_id}",
    "upcoming": "/calendar/upcoming",
    "availability": "/calendar/availability",
    "tools": "/meetings/agent-tools",
    "docs": "/docs"
  }
}
```

**✅ Success Criteria:**
- Version: "1.0.0"
- Status: "active"
- All endpoint paths listed

---

### **Test 3: AI Agent Tools Verification**

**Objective**: Verify all 5 vLLM function calling tools are available

```bash
curl http://localhost:5000/meetings/agent-tools | python -m json.tool
```

**Expected Response:**
```json
{
  "tools": [
    {
      "name": "get_calendar_availability",
      "description": "Get calendar availability for participants in a date range",
      "parameters": ["participant_emails", "start_date", "end_date", "duration_minutes"]
    },
    {
      "name": "analyze_optimal_slots",
      "description": "Analyze availability data and recommend optimal meeting slots",
      "parameters": ["availability_data", "meeting_requirements", "max_suggestions"]
    },
    {
      "name": "create_calendar_event",
      "description": "Create a calendar event for confirmed meeting",
      "parameters": ["title", "description", "start_time", "end_time", "attendees", "location"]
    },
    {
      "name": "send_meeting_email",
      "description": "Send meeting proposal or confirmation email",
      "parameters": ["to", "subject", "body", "html_body", "email_type"]
    },
    {
      "name": "check_email_responses",
      "description": "Check for email responses related to meeting proposals",
      "parameters": ["proposal_id", "query", "max_results"]
    }
  ],
  "total_tools": 5
}
```

**✅ Success Criteria:**
- Total tools: 5
- All tool names present
- Each tool has description and parameters

---

### **Test 4: Calendar Integration Test**

**Objective**: Verify Google Calendar API integration

```bash
curl http://localhost:5000/calendar/upcoming?days_ahead=7 | python -m json.tool
```

**Expected Response:**
```json
{
  "meetings": [
    {
      "id": "event_123",
      "title": "Existing Meeting",
      "description": "Sample meeting",
      "start_time": "2025-01-06T10:00:00+00:00",
      "end_time": "2025-01-06T11:00:00+00:00",
      "attendees": ["user@example.com"],
      "location": "",
      "formatted": "Monday, January 06 at 10:00 AM - 11:00 AM"
    }
  ],
  "total_count": 1,
  "date_range": {
    "start": "2025-01-05T10:00:00.000000",
    "end": "2025-01-12T23:59:59.000000",
    "days": 7
  }
}
```

**✅ Success Criteria:**
- Returns meeting list (may be empty)
- Correct date range
- Proper formatting

---

### **Test 5: Calendar Availability Check**

**Objective**: Test availability checking for participants

```bash
curl "http://localhost:5000/calendar/availability?participant_emails=test@example.com&days_ahead=7&duration_minutes=30" | python -m json.tool
```

**Expected Response:**
```json
{
  "success": true,
  "availability_data": [
    {
      "participant_email": "test@example.com",
      "free_slots": [
        {
          "start_time": "2025-01-06T09:00:00",
          "end_time": "2025-01-06T10:00:00",
          "available": true,
          "timezone": "UTC"
        }
      ],
      "busy_slots": [
        {
          "start_time": "2025-01-06T14:00:00",
          "end_time": "2025-01-06T15:00:00",
          "available": false,
          "timezone": "UTC"
        }
      ]
    }
  ],
  "error": null
}
```

**✅ Success Criteria:**
- Success: true
- Availability data returned
- Free and busy slots listed

---

### **Test 6: Meeting Scheduling (Core Functionality)**

**Objective**: Test the main AI-powered meeting scheduling feature

**6.1 Basic Meeting Request**
```bash
curl -X POST http://localhost:5000/meetings/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Meeting",
    "description": "API testing meeting",
    "duration_minutes": 30,
    "organizer": {
      "name": "Test User",
      "email": "test.user@example.com",
      "timezone": "America/New_York"
    },
    "participants": [
      {
        "name": "Participant One",
        "email": "participant1@example.com",
        "timezone": "America/New_York"
      }
    ],
    "priority": "medium",
    "preferred_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
    "user_preferences": {
      "work_start_hour": 9,
      "work_end_hour": 17,
      "buffer_time_minutes": 15
    }
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "proposal_id": "abc123-def456-ghi789",
  "suggested_slots": [
    {
      "start_time": "2025-01-07T14:00:00",
      "end_time": "2025-01-07T14:30:00",
      "formatted": "Tuesday, January 07 at 02:00 PM - 02:30 PM"
    },
    {
      "start_time": "2025-01-07T15:00:00",
      "end_time": "2025-01-07T15:30:00",
      "formatted": "Tuesday, January 07 at 03:00 PM - 03:30 PM"
    }
  ],
  "reasoning": "Selected afternoon slots to avoid lunch hours and respect all participants' working hours in Eastern timezone.",
  "agent_message": "Found 2 optimal time slots considering all constraints and preferences."
}
```

**✅ Success Criteria:**
- Success: true
- Proposal ID generated
- Multiple time slots suggested
- AI reasoning provided

---

### **Test 7: Proposal Management**

**Objective**: Test proposal retrieval and management

**7.1 Get Proposal Status**
```bash
# Use proposal_id from previous test
curl http://localhost:5000/meetings/proposal/abc123-def456-ghi789 | python -m json.tool
```

**Expected Response:**
```json
{
  "proposal_id": "abc123-def456-ghi789",
  "status": "pending",
  "meeting_title": "Test Meeting",
  "participants": [
    "test.user@example.com",
    "participant1@example.com"
  ],
  "suggested_slots": [
    {
      "index": 0,
      "start_time": "2025-01-07T14:00:00",
      "end_time": "2025-01-07T14:30:00",
      "formatted": "Tuesday, January 07 at 02:00 PM - 02:30 PM"
    }
  ],
  "reasoning": "Selected afternoon slots to avoid lunch hours...",
  "created_at": "2025-01-05T10:00:00.000000"
}
```

**✅ Success Criteria:**
- Correct proposal ID
- Status: "pending"
- All meeting details present

---

### **Test 8: Meeting Confirmation**

**Objective**: Test meeting confirmation and calendar event creation

**8.1 Confirm Meeting**
```bash
# Use proposal_id and select slot index 0
curl -X POST "http://localhost:5000/meetings/confirm/abc123-def456-ghi789?selected_slot_index=0&confirmed_by=test_user" | python -m json.tool
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Meeting confirmed successfully",
  "proposal_id": "abc123-def456-ghi789",
  "confirmed_slot": {
    "start_time": "2025-01-07T14:00:00",
    "end_time": "2025-01-07T14:30:00",
    "formatted": "Tuesday, January 07 at 02:00 PM - 02:30 PM"
  },
  "calendar_event_id": "cal_event_123456",
  "emails_sent": true,
  "participants_notified": [
    "test.user@example.com",
    "participant1@example.com"
  ]
}
```

**✅ Success Criteria:**
- Success: true
- Calendar event created
- Email confirmations sent
- All participants notified

---

### **Test 9: Advanced Scenarios**

**9.1 Multi-Participant Meeting**
```bash
curl -X POST http://localhost:5000/meetings/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Standup",
    "description": "Daily team synchronization",
    "duration_minutes": 60,
    "organizer": {
      "name": "Team Lead",
      "email": "lead@company.com",
      "timezone": "America/Los_Angeles"
    },
    "participants": [
      {
        "name": "Developer 1",
        "email": "dev1@company.com",
        "timezone": "America/New_York"
      },
      {
        "name": "Developer 2", 
        "email": "dev2@company.com",
        "timezone": "Europe/London"
      },
      {
        "name": "Designer",
        "email": "designer@company.com",
        "timezone": "Asia/Tokyo"
      }
    ],
    "priority": "high",
    "preferred_days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  }'
```

**✅ Success Criteria:**
- Handles multiple timezones
- Finds overlapping availability
- Provides intelligent suggestions

**9.2 High Priority Meeting**
```bash
curl -X POST http://localhost:5000/meetings/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Urgent Client Call",
    "description": "Critical issue resolution",
    "duration_minutes": 45,
    "organizer": {
      "name": "Account Manager",
      "email": "manager@company.com"
    },
    "participants": [
      {
        "name": "Technical Lead",
        "email": "tech@company.com"
      }
    ],
    "priority": "urgent"
  }'
```

**✅ Success Criteria:**
- Prioritizes urgent meetings
- Finds earliest available slots
- Accommodates shorter notice

---

### **Test 10: Error Handling**

**10.1 Invalid Meeting Request**
```bash
curl -X POST http://localhost:5000/meetings/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "duration_minutes": 5
  }'
```

**Expected Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    },
    {
      "loc": ["body", "duration_minutes"],
      "msg": "ensure this value is greater than or equal to 15",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

**10.2 Invalid Proposal ID**
```bash
curl http://localhost:5000/meetings/proposal/invalid-id | python -m json.tool
```

**Expected Response:**
```json
{
  "detail": "Proposal not found"
}
```

**✅ Success Criteria:**
- Proper validation errors
- Clear error messages
- Appropriate HTTP status codes

---

### **Test 11: Documentation Access**

**11.1 Swagger UI**
```bash
# Open in browser
curl http://localhost:5000/docs
```

**11.2 ReDoc**
```bash
# Open in browser  
curl http://localhost:5000/redoc
```

**11.3 OpenAPI Schema**
```bash
curl http://localhost:5000/openapi.json | python -m json.tool
```

**✅ Success Criteria:**
- Documentation loads successfully
- All endpoints documented
- Interactive testing available

---

## 📊 **Testing Checklist**

### **Core Functionality Tests**
- [ ] **System Health**: All services operational
- [ ] **API Access**: Root endpoint accessible
- [ ] **AI Tools**: All 5 function calling tools available
- [ ] **Calendar Integration**: Can read calendar events
- [ ] **Meeting Scheduling**: Can create meeting proposals
- [ ] **Proposal Management**: Can retrieve and track proposals
- [ ] **Meeting Confirmation**: Can confirm and create events
- [ ] **Email Integration**: Notifications sent successfully

### **Advanced Feature Tests**
- [ ] **Multi-Timezone**: Handles different timezones correctly
- [ ] **Multi-Participant**: Supports multiple attendees
- [ ] **Priority Handling**: Respects meeting priorities
- [ ] **Preference Alignment**: Considers user preferences
- [ ] **Conflict Resolution**: Handles scheduling conflicts

### **Error Handling Tests**
- [ ] **Input Validation**: Rejects invalid requests
- [ ] **Missing Data**: Handles incomplete information
- [ ] **API Errors**: Graceful degradation on failures
- [ ] **Authentication**: Handles OAuth errors

### **Performance Tests**
- [ ] **Response Time**: < 5 seconds for scheduling
- [ ] **Concurrent Requests**: Handles multiple users
- [ ] **Resource Usage**: Reasonable memory/CPU consumption

---

## 🎯 **Success Metrics**

### **Functional Success Criteria**
1. ✅ All API endpoints return 200 status for valid requests
2. ✅ AI agent successfully analyzes calendar availability
3. ✅ Optimal time slots are suggested with reasoning
4. ✅ Calendar events are created upon confirmation
5. ✅ Email notifications are sent to all participants
6. ✅ Multi-timezone meetings are handled correctly

### **Technical Success Criteria**
1. ✅ All 5 vLLM function calling tools operational
2. ✅ Google Calendar and Gmail APIs integrated
3. ✅ FastAPI server with comprehensive documentation
4. ✅ Proper error handling and validation
5. ✅ Secure credential management
6. ✅ Comprehensive logging for debugging

### **Performance Success Criteria**
1. ✅ API response time < 5 seconds for meeting scheduling
2. ✅ Support for up to 20 participants per meeting
3. ✅ Handles 100+ requests per minute
4. ✅ 99.9% uptime target
5. ✅ Graceful degradation on external API failures

---

## 🔧 **Troubleshooting Common Issues**

### **Startup Issues**
- **Port in use**: `lsof -ti:8000 | xargs kill -9`
- **Missing credentials**: Check `.env` and `credentials.json`
- **OAuth errors**: Re-run Google authentication flow

### **API Issues**
- **500 errors**: Check logs in `logs/scheduleai.log`
- **Calendar errors**: Verify Google API permissions
- **vLLM errors**: Check vLLM server status and connectivity

### **Testing Issues**
- **Connection refused**: Ensure server is running
- **Permission denied**: Check Google OAuth scopes
- **Timeout errors**: Increase request timeout

---

This comprehensive testing guide ensures that SchedulAI meets all functional and technical requirements while providing a robust, reliable meeting scheduling solution. 