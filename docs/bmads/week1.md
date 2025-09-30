# BMAD — Breakdown & Backlog → Mock & Model → Automate & Assemble → Document & Deploy

## Breakdown & Backlog
- Endpoints: /match, /apply-pack, /outreach-plan, /followups/run, /summary/today
- Tools: sheets_adapter, gmail_stub, calendar_stub
- SLA: Apply within 24h of 'DateFound'

## Mock & Model
- Pydantic schemas in data/schemas
- Prompts in agents/prompts
- crew.yaml defines orchestration

## Automate & Assemble
- Implement real LLM calls and tools wiring
- Cron scripts for ingest and summary

## Document & Deploy
- README quickstart, logs to apps/backend/logs/app.log
