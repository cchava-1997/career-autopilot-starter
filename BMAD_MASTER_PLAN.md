# BMAD Master Plan - Career Autopilot

## 🎯 Project Overview
Build a robust, Mac-friendly web app that runs job search end-to-end with strict separation of concerns, accessibility, and security.

## 📋 Milestone Plan

### M1: Core UI + API Foundation (Week 1)
- **Epic 1.1**: Project scaffolding & environment setup
- **Epic 1.2**: UI shell with navigation & accessibility
- **Epic 1.3**: Backend API foundation with Pydantic models
- **Epic 1.4**: Basic CRUD operations for core entities

### M2: Resume Vault & Overleaf Integration (Week 2)
- **Epic 2.1**: Resume management UI (tracks: PO/PM/TPM)
- **Epic 2.2**: Overleaf Git-Bridge integration
- **Epic 2.3**: A4 PDF build with tight whitespace
- **Epic 2.4**: Resume versioning and defaults

### M3: Job Management & Apply Pack (Week 3)
- **Epic 3.1**: Job sources management UI
- **Epic 3.2**: Jobs table with SLA tracking
- **Epic 3.3**: Apply Pack generation (JD → bullets + cover)
- **Epic 3.4**: File management and persistence

### M4: Outreach & Autofill (Week 4)
- **Epic 4.1**: Outreach planning (2+2+1 contacts)
- **Epic 4.2**: Message drafting and follow-up scheduling
- **Epic 4.3**: Playwright autofill worker
- **Epic 4.4**: ATS detection and field mapping

### M5: Summary, Skills & Hardening (Week 5)
- **Epic 5.1**: Daily summary generation
- **Epic 5.2**: Skills gap analysis
- **Epic 5.3**: Settings and secrets management
- **Epic 5.4**: Testing, logging, and documentation

## 🗂️ Proposed Folder Structure

```
career-autopilot-starter/
├── apps/
│   ├── frontend/                 # React/Next.js UI
│   │   ├── src/
│   │   │   ├── components/       # Reusable UI components
│   │   │   ├── pages/           # Route pages
│   │   │   ├── hooks/           # Custom React hooks
│   │   │   ├── services/        # API client
│   │   │   ├── store/           # State management
│   │   │   └── utils/           # Helper functions
│   │   ├── public/              # Static assets
│   │   └── package.json
│   └── backend/                 # FastAPI backend
│       ├── main.py              # FastAPI app
│       ├── api/                 # API routes
│       ├── models/              # Pydantic models
│       ├── services/            # Business logic
│       └── logs/                # JSONL logs
├── workers/                     # Background workers
│   ├── autofill/               # Playwright autofill
│   ├── overleaf/               # Overleaf build worker
│   └── outreach/               # Outreach automation
├── data/                       # Application data
│   ├── applications/           # Job application files
│   ├── resumes/               # Resume versions
│   ├── schemas/               # Pydantic schemas
│   └── templates/             # LaTeX templates
├── agents/                     # CrewAI agents (optional)
│   ├── prompts/               # System prompts
│   └── crew.yaml              # Crew configuration
├── tools/                      # External tool adapters
│   ├── overleaf.py            # Overleaf API client
│   ├── sheets_adapter.py      # Google Sheets
│   ├── gmail_stub.py          # Gmail integration
│   └── calendar_stub.py       # Calendar integration
├── scripts/                    # Utility scripts
│   ├── setup.sh               # Environment setup
│   ├── test.sh                # Test runner
│   └── deploy.sh              # Deployment script
├── tests/                      # Test suites
│   ├── api/                   # API tests
│   ├── ui/                    # UI tests
│   ├── workers/               # Worker tests
│   └── e2e/                   # End-to-end tests
├── docs/                       # Documentation
│   ├── bmads/                 # BMAD notes per epic
│   ├── runbooks/              # Operational guides
│   └── api/                   # API documentation
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
├── package.json              # Node dependencies
├── docker-compose.yml        # Local development
└── README.md                 # Quickstart guide
```

## 🔧 Environment Variables (.env template)

```bash
# === Core Application ===
APP_ENV=development
APP_DEBUG=true
APP_SECRET_KEY=your-secret-key-here

# === Database & Storage ===
DATABASE_URL=sqlite:///./data/app.db
TRACKER_PATH=/Users/ptg/Documents/career_autopilot_tracker.xlsx
APPLY_PACK_DIR=./data/applications
RESUME_DIR=./data/resumes

# === Overleaf Integration ===
OVERLEAF_API_URL=https://www.overleaf.com/api/v1
OVERLEAF_API_KEY=your-overleaf-api-key
OVERLEAF_PROJECT_PO=your-po-project-id
OVERLEAF_PROJECT_PM=your-pm-project-id
OVERLEAF_PROJECT_TPM=your-tpm-project-id

# === Browser Automation ===
CHROME_USER_DATA_DIR=/Users/ptg/Library/Application Support/Google/Chrome/Autopilot
PLAYWRIGHT_BROWSER_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome

# === Profile Information ===
PROFILE_NAME="Your Name"
PROFILE_EMAIL="your.email@example.com"
PROFILE_PHONE="+1-555-123-4567"
PROFILE_LINKEDIN="https://linkedin.com/in/yourprofile"

# === External Services ===
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-client-secret
GOOGLE_CALENDAR_ID=your-calendar-id
SHEETS_SPREADSHEET_ID=your-sheets-id

# === Logging & Monitoring ===
LOG_LEVEL=INFO
LOG_FILE=./apps/backend/logs/app.log.jsonl
SENTRY_DSN=your-sentry-dsn

# === Development ===
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📊 JSONL Logging Format

```json
{"ts": "2025-01-15T10:30:00Z", "type": "api_request", "actor": "user", "job_id": "job_001", "step": "match", "status": "success", "metadata": {"endpoint": "/match", "response_time_ms": 150}}
{"ts": "2025-01-15T10:31:00Z", "type": "autofill", "actor": "system", "job_id": "job_001", "step": "field_mapping", "status": "partial", "metadata": {"ats_type": "workday", "fields_filled": 8, "fields_total": 12}}
{"ts": "2025-01-15T10:32:00Z", "type": "overleaf_build", "actor": "system", "job_id": "job_001", "step": "pdf_generation", "status": "success", "metadata": {"track": "PM", "pages": 2, "build_time_s": 45}}
```

## 🚨 Error Handling Patterns

### API Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid job ID format",
    "details": {
      "field": "job_id",
      "value": "invalid-id",
      "constraint": "must be alphanumeric with underscores"
    },
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_123456"
  }
}
```

### UI Error States
- **Toast notifications** for transient errors
- **Inline validation** for form errors
- **Error boundaries** for component failures
- **Retry mechanisms** for network failures
- **Fallback UI** for critical failures

## 🎯 Acceptance Criteria

### Technical Requirements
- [ ] All endpoints typed with Pydantic models
- [ ] OpenAPI documentation auto-generated
- [ ] A11y compliance (WCAG 2.1 AA)
- [ ] Keyboard navigation support
- [ ] Responsive design (mobile-friendly)
- [ ] Error handling with clear user feedback
- [ ] JSONL logging for all actions
- [ ] No secrets in code repository

### Functional Requirements
- [ ] Resume vault with 3 tracks (PO/PM/TPM)
- [ ] Overleaf integration with A4 PDF build
- [ ] Job sources management
- [ ] Jobs table with SLA tracking
- [ ] Apply pack generation and editing
- [ ] Outreach planning (2+2+1 contacts)
- [ ] Autofill worker with ATS detection
- [ ] Daily summary generation
- [ ] Skills gap analysis
- [ ] Settings management

### Demo Flow
1. Add job → prepare pack → build resume PDF
2. Autofill ATS → pause before final submit
3. User reviews → clicks final submit
4. Mark applied → generate summary
5. Complete end-to-end workflow

## 🔄 Next Steps

1. **Approve this plan** - Review and confirm the structure
2. **Generate scaffolding** - Create folder structure and base files
3. **Set up environment** - Configure .env and dependencies
4. **Begin M1 implementation** - Start with core UI + API foundation

---

*This plan follows BMAD methodology: Breakdown & Backlog → Mock & Model → Automate & Assemble → Document & Deploy*
