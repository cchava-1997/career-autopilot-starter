# Career Autopilot — Complete Job Search Automation

A robust, Mac-friendly web application that automates your entire job search workflow from resume management to ATS autofill.

## 🎯 Features

- **Resume Vault**: Manage multiple resume tracks (PO/PM/TPM) with Overleaf integration
- **Job Sources**: Add and manage job boards and ATS portals
- **Jobs Table**: Track applications with SLA monitoring (apply within 24h)
- **Apply Pack**: Generate tailored bullet points and cover letters
- **Outreach**: Automated 2+2+1 contact strategy with message drafts
- **Autofill**: ATS form filling with browser automation (stops before final submit)
- **Daily Summary**: Six-line digest with skills gap analysis
- **Secure Settings**: Environment-based configuration with no secrets in code

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop
- Docker Compose

**Installation:**
```bash
git clone <repository-url>
cd career-autopilot-starter
./scripts/docker-setup.sh
```

**Access application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development (Recommended for Development)

**Prerequisites:**
- macOS with Python 3.10+
- Node.js 18+
- Chrome browser
- BasicTeX or MacTeX

**Quick Start:**
```bash
git clone <repository-url>
cd career-autopilot-starter
./scripts/dev.sh
```

**Manual Setup:**
```bash
# Install dependencies
./scripts/setup.sh

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Start services manually
# Terminal 1: Backend
source .venv/bin/activate
uvicorn apps.backend.main:app --reload

# Terminal 2: Frontend
cd apps/frontend
npm run dev
```

**Access application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
career-autopilot-starter/
├── apps/
│   ├── frontend/          # Next.js React application
│   └── backend/           # FastAPI backend
├── workers/               # Background workers
│   ├── autofill/         # Playwright ATS automation
│   ├── overleaf/         # Overleaf PDF builds
│   └── outreach/         # Outreach automation
├── data/                  # Application data
│   ├── applications/     # Job application files
│   ├── resumes/         # Resume versions
│   └── templates/       # LaTeX templates
├── tools/                # External integrations
├── tests/                # Test suites
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## 🔧 Configuration

### Environment Variables

Key configuration in `.env`:

```bash
# Overleaf Integration
OVERLEAF_API_KEY=your-overleaf-api-key
OVERLEAF_PROJECT_PO=your-po-project-id
OVERLEAF_PROJECT_PM=your-pm-project-id
OVERLEAF_PROJECT_TPM=your-tpm-project-id

# Browser Automation
CHROME_USER_DATA_DIR=/path/to/chrome/profile
PLAYWRIGHT_BROWSER_PATH=/path/to/chrome

# Profile Information
PROFILE_NAME="Your Name"
PROFILE_EMAIL="your.email@example.com"
PROFILE_PHONE="+1-555-123-4567"
```

### Overleaf Setup

1. Create Overleaf projects for each track (PO/PM/TPM)
2. Add `\input{_layout_autogen.tex}` to your LaTeX templates
3. Configure project IDs in `.env`
4. Test builds with `POST /overleaf/build`

### Chrome Profile Setup

1. Create dedicated Chrome profile for autofill
2. Log into your ATS accounts (Workday, Greenhouse, etc.)
3. Set `CHROME_USER_DATA_DIR` to profile path
4. Test with `POST /autofill/run`

## 🎯 Usage Workflow

### 1. Add Job
```bash
curl -X POST "http://localhost:8000/jobs/add" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "job_001",
    "company": "TechCorp",
    "role": "Senior PM",
    "jd_url": "https://example.com/job",
    "track": "PM"
  }'
```

### 2. Prepare Apply Pack
```bash
curl -X POST "http://localhost:8000/apply/prepare" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "job_001",
    "company": "TechCorp",
    "role": "Senior PM",
    "track": "PM",
    "jd_text": "Job description text..."
  }'
```

### 3. Build Resume PDF
```bash
curl -X POST "http://localhost:8000/overleaf/build" \
  -H "Content-Type: application/json" \
  -d '{
    "track": "PM",
    "job_id": "job_001"
  }'
```

### 4. Autofill ATS
```bash
curl -X POST "http://localhost:8000/autofill/run" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "job_001",
    "url": "https://company.workday.com/apply",
    "track": "PM"
  }'
```

### 5. Generate Summary
```bash
curl -X POST "http://localhost:8000/summary/today"
```

## 🧪 Testing

### Docker Testing
```bash
# Run tests in Docker
docker-compose exec backend python -m pytest tests/api/ -v
docker-compose exec frontend npm test
```

### Local Testing
```bash
# Run all tests
./scripts/test.sh

# Individual test suites
python -m pytest tests/api/ -v
cd apps/frontend && npm test
python -m pytest tests/e2e/ -v
```

## 📚 Documentation

- [BMAD Master Plan](BMAD_MASTER_PLAN.md) - Development methodology
- [M1: Core UI + API](docs/bmads/m1_core_ui_api.md) - Foundation milestone
- [Overleaf Build Runbook](docs/runbooks/overleaf_build.md) - Troubleshooting
- [API Documentation](http://localhost:8000/docs) - Interactive API docs

## 🔒 Security

- No passwords or secrets in code repository
- Environment-based configuration
- Local browser session for ATS authentication
- JSONL logging for audit trails
- Input validation and sanitization

## 🚨 Troubleshooting

### Docker Issues

1. **Services Not Starting**
   ```bash
   # Check service status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   
   # Restart services
   docker-compose restart
   ```

2. **Port Conflicts**
   ```bash
   # Stop all services
   docker-compose down
   
   # Check for port usage
   lsof -i :3000
   lsof -i :8000
   
   # Kill conflicting processes
   kill -9 <PID>
   ```

3. **Build Issues**
   ```bash
   # Rebuild without cache
   docker-compose build --no-cache
   
   # Clean up Docker
   docker system prune -a
   ```

### Common Issues

1. **Overleaf Build Fails**
   - Check API key and project IDs
   - Verify LaTeX template syntax
   - Review build logs: `docker-compose logs backend`

2. **Autofill Not Working**
   - Verify Chrome profile path
   - Check ATS login status
   - Review field selectors in `workers/autofill/`

3. **Frontend Not Loading**
   - Check Node.js version (18+)
   - Clear npm cache: `npm cache clean --force`
   - Reinstall dependencies: `rm -rf node_modules && npm install`

### Logs

**Docker logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Local logs:**
```bash
tail -f apps/backend/logs/app.log.jsonl
```

## 🤝 Contributing

1. Follow BMAD methodology
2. Write tests for new features
3. Update documentation
4. Ensure accessibility compliance
5. Follow security best practices

## 📄 License

MIT License - see LICENSE file for details.

## 🎯 Roadmap

- [ ] M2: Resume Vault & Overleaf Integration
- [ ] M3: Job Management & Apply Pack
- [ ] M4: Outreach & Autofill
- [ ] M5: Summary, Skills & Hardening
- [ ] CrewAI Orchestration (Optional)

---

**Happy job hunting! 🎯**