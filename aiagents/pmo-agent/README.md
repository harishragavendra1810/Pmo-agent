# PMO Agent - AI-Powered Project Management Office System

An intelligent FastAPI-based system that automates project management tasks using OpenAI GPT-4, including Change Request management, Project Planning, and RAID (Risks, Assumptions, Issues, Dependencies) tracking.

## Features

### 🔄 **CR Agent** (Change Request Management)
- Automatically identifies scope changes by comparing Original SOW with current discussions
- Generates structured Change Requests with impact analysis (cost, timeline, scope)
- Integrates with JIRA for ticket tracking
- Validates and prioritizes change requests (HIGH/MEDIUM/LOW)

### 📋 **Plan Agent** (Project Planning)
- Creates detailed project plans from scope documents and meeting notes
- Generates task breakdowns with timelines and dependencies
- Optimizes schedules using critical path analysis
- Uploads to Smartsheet for team collaboration

### ⚠️ **RAID Agent** (Risk, Assumptions, Issues, Dependencies)
- Identifies project risks and mitigation strategies
- Tracks assumptions and project dependencies
- Categorizes and prioritizes items by severity
- Exports to Excel/Smartsheet for stakeholder visibility

## Architecture

```
pmo-agent/
├── src/
│   ├── agents/           # CR, Plan, RAID agents
│   ├── integrations/     # JIRA, Smartsheet, Excel connectors
│   ├── services/         # OpenAI service, Document processing
│   ├── models/           # Pydantic data models
│   ├── utils/            # Logging, helpers
│   ├── config.py         # Configuration management
│   └── main.py           # FastAPI application
├── tests/                # Unit and integration tests
├── data/                 # Sample data/mock files
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key
- JIRA/Smartsheet API tokens (optional)

### Installation

1. **Clone or navigate to the project:**
```bash
cd pmo-agent
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or: source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Endpoints

### 1. Health Check
```http
GET /health
```

### 2. Generate Change Request
```http
POST /api/v1/change-request
Content-Type: application/json

{
  "project_id": "PROJ-001",
  "sow": "Original scope of work...",
  "current_content": "Meeting transcript or email..."
}
```

**Response:**
```json
{
  "status": "SUCCESS",
  "message": "Change request generated successfully",
  "data": {
    "cr": {
      "title": "Add Export Feature",
      "description": "Client requested PDF export capability",
      "scope_impact": "Adds 2 new modules",
      "cost_impact": 5000,
      "timeline_impact": "Add 10 days",
      "priority": "HIGH"
    },
    "jira_ticket": "PMO-ADD-001",
    "excel_file": "outputs/CR_PROJ-001_20240411_120000.json"
  }
}
```

### 3. Generate Project Plan
```http
POST /api/v1/project-plan
Content-Type: application/json

{
  "project_id": "PROJ-001",
  "project_name": "Website Redesign",
  "sow": "Scope of work document...",
  "meeting_notes": "Kick-off meeting notes..."
}
```

### 4. Generate RAID Log
```http
POST /api/v1/raid-log
Content-Type: application/json

{
  "project_id": "PROJ-001",
  "project_name": "Website Redesign",
  "project_context": "Project overview...",
  "plan": { /* project plan data */ }
}
```

### 5. Full Analysis (All Three Agents)
```http
POST /api/v1/full-analysis
Content-Type: application/json

{
  "project_id": "PROJ-001",
  "project_name": "Website Redesign",
  "sow": "Scope document...",
  "meeting_transcript": "Latest meeting...",
  "kickoff_notes": "Initial kick-off notes..."
}
```

## Configuration

### Environment Variables (.env)

```env
# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# JIRA
JIRA_SERVER=https://your-jira.atlassian.net
JIRA_USERNAME=email@company.com
JIRA_API_TOKEN=your_token
JIRA_ENABLED=False  # Set True to enable

# Smartsheet
SMARTSHEET_API_TOKEN=your_token
SMARTSHEET_ENABLED=False  # Set True to enable

# Excel
EXCEL_OUTPUT_PATH=./outputs/

# Logging
LOG_LEVEL=INFO
DEBUG_MODE=False

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## Project Structure

### Models (src/models/pmo_models.py)
- `ChangeRequest` - CR with impact analysis
- `ProjectPlan` - Complete project plan with tasks
- `PlannedTask` - Individual project tasks
- `RAIDLog` - Collection of RAID items
- `RAIDItem` - Individual risk/assumption/issue/dependency
- `ProcessedInput` - Normalized input data
- `PMOAgentResponse` - Standard API response

### Agents

#### CR Agent (src/agents/cr_agent.py)
- Compares SOW with new content using AI
- Generates CRs with priority and impact
- Validates CR structure
- Estimates CR impact

#### Plan Agent (src/agents/plan_agent.py)
- Generates task-level project plans
- Optimizes schedules with dependencies
- Calculates duration and effort
- Validates plan completeness

#### RAID Agent (src/agents/raid_agent.py)
- Identifies risks, assumptions, issues, dependencies
- Prioritizes by severity
- Suggests mitigation plans
- Categorizes items

### Integrations

- **JIRA Integration** - Create/update change request tickets
- **Smartsheet Integration** - Upload plans and RAID logs
- **Excel Integration** - Save outputs as JSON/Excel files

## Running Tests

```bash
pytest tests/ -v
```

## Example Usage

### Python Client Example
```python
import httpx

client = httpx.Client(base_url="http://localhost:8000")

# Generate CR
response = client.post("/api/v1/change-request", json={
    "project_id": "PROJ-001",
    "sow": "Original scope...",
    "current_content": "Client wants feature X..."
})

print(response.json())
```

### cURL Example
```bash
curl -X POST http://localhost:8000/api/v1/change-request \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "PROJ-001",
    "sow": "Original scope...",
    "current_content": "Client wants feature X..."
  }'
```

## Integration Guide

### Enabling JIRA Integration
1. Get your JIRA API token from: https://id.atlassian.com/manage-profile/security/api-tokens
2. Set in .env:
   ```env
   JIRA_ENABLED=True
   JIRA_SERVER=https://your-instance.atlassian.net
   JIRA_USERNAME=your_email@company.com
   JIRA_API_TOKEN=your_token
   ```

### Enabling Smartsheet Integration
1. Get API token from Smartsheet account settings
2. Set in .env:
   ```env
   SMARTSHEET_ENABLED=True
   SMARTSHEET_API_TOKEN=your_token
   ```

## Troubleshooting

### OpenAI Connection Error
- Verify OPENAI_API_KEY is set correctly
- Check API key has sufficient credits
- Ensure key has GPT-4 access

### JIRA Integration Fails
- Verify server URL format (include https://)
- Check API token is valid and not expired
- Ensure user has permission to create issues

### Smartsheet Upload Fails
- Verify API token is active
- Check workspace permissions
- Ensure target worksheet exists

## Development

### Project Structure
```bash
# Create new agent
touch src/agents/new_agent.py

# Create integration
touch src/integrations/new_integration.py

# Create test
touch tests/test_new_feature.py
```

### Best Practices
- Use async/await for I/O operations
- Validate all inputs with Pydantic
- Log all significant operations
- Handle errors gracefully with PMOAgentResponse
- Write unit tests for new features

## Performance Notes

- OpenAI API calls are rate-limited (monitor for 429 errors)
- Large documents (>8000 tokens) may be truncated
- JIRA/Smartsheet operations depend on network latency
- Responses typically take 5-30 seconds depending on API loads

## License

MIT License - See LICENSE file

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in `pmo_agent.log`
3. Check API documentation at `/docs`
4. Submit issues with error messages and reproduction steps

---

**Version:** 1.0.0  
**Last Updated:** April 2024
