from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import datetime, timedelta
import os, json, pathlib
from dotenv import load_dotenv

# Import new API routes
from .api.jobs import router as jobs_router
from .api.resumes import router as resumes_router
from .api.overleaf import router as overleaf_router
from .api.sources import router as sources_router
from .api.dashboard import router as dashboard_router
from .api.auth import router as auth_router
from .api.linkedin_auth import router as linkedin_auth_router
from .api.linkedin_playwright_auth import router as linkedin_playwright_auth_router

load_dotenv()

app = FastAPI(
    title="Career Autopilot API", 
    version="0.1.0",
    description="Complete job search automation platform"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(jobs_router)
app.include_router(resumes_router)
app.include_router(overleaf_router)
app.include_router(sources_router)
app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(linkedin_auth_router)
app.include_router(linkedin_playwright_auth_router)

LOG_PATH = pathlib.Path("apps/backend/logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)

def log_event(event: dict):
    (LOG_PATH / "app.log").open("a").write(json.dumps(event) + "\n")

class BulletRewrite(BaseModel):
    original: str
    rewritten: str
    rationale: str

class JDMatchRequest(BaseModel):
    resume_text: str
    jd_text: str
    target_role: str
    seniority: str

class JDMatchResponse(BaseModel):
    match_score: float
    missing_skills: List[str]
    rewritten_bullets: List[BulletRewrite]
    cover_letter: str
    risks: List[str]

class ApplyPackRequest(BaseModel):
    job_id: str
    company: str
    role: str
    match: JDMatchResponse
    base_resume_bullets: List[str]

class OutreachContact(BaseModel):
    name: str
    role: str
    company: str
    channel: Literal["linkedin","email"]
    profile_url: Optional[str] = None
    email: Optional[str] = None
    persona: Literal["peer","insider","recruiter","referral"]

class OutreachPlan(BaseModel):
    job_id: str
    contacts: List[OutreachContact]
    messages: dict  # name -> message
    followups: dict # name -> ISO datetime

@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.utcnow().isoformat()}

@app.post("/match", response_model=JDMatchResponse)
def match(req: JDMatchRequest):
    # Stub logic: deterministic placeholders. Wire LLM later.
    # Simple heuristic for demo
    score = 0.62
    missing = ["A/B testing", "Amplitude/GA4", "SQL window functions"]
    # fake rewrite using the first three bullets if available in resume
    sample_original = req.resume_text.split("\n")
    bw = []
    for i, line in enumerate(sample_original[:3] or ["Improved process", "Led team", "Shipped feature"]):
        bw.append(BulletRewrite(
            original=line.strip(),
            rewritten=f"{line.strip()} — translated to JD impact (revenue, speed, quality).",
            rationale="Aligns to JD keywords; emphasizes outcomes and metrics."
        ))
    cover = (
        f"""Hi Team — applying for {req.target_role}. I’ve shipped AI/IoT/analytics products with clear outcomes: 
        - Reduced onboarding time from 30min → 5min for 10k+ devices (WhyGrene)
        - Led $1M AI assistant program (Brownells) improving decisions & adoption
        - Built Azure B2C auth and data pipelines across teams
        Looking forward to a quick screen to confirm fit.
        """
    )
    resp = JDMatchResponse(
        match_score=score,
        missing_skills=missing,
        rewritten_bullets=bw,
        cover_letter=cover,
        risks=["Role may require deeper marketplace metrics; add A/B test story"],
    )
    log_event({"type":"match", "req": req.model_dump(), "resp": resp.model_dump()})
    return resp

@app.post("/apply-pack")
def apply_pack(req: ApplyPackRequest):
    # Render files for the job (placeholder write)
    outdir = pathlib.Path(os.getenv("APPLY_PACK_DIR", "./data/applications")) / req.job_id
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "cover_letter.txt").write_text(req.match.cover_letter.strip())
    (outdir / "bullets.json").write_text(json.dumps([br.model_dump() for br in req.match.rewritten_bullets], indent=2))
    log_event({"type":"apply_pack", "job_id": req.job_id, "company": req.company, "role": req.role, "path": str(outdir)})
    return {"ok": True, "path": str(outdir)}

@app.post("/outreach-plan", response_model=OutreachPlan)
def outreach_plan(job_id: str, company: str, role: str):
    # Generate 2 peers, 2 insiders, 1 recruiter stubs
    contacts = [
        OutreachContact(name="Peer One", role="PM II", company=company, channel="linkedin", persona="peer"),
        OutreachContact(name="Peer Two", role="Sr PM", company=company, channel="linkedin", persona="peer"),
        OutreachContact(name="Insider One", role="Eng Manager", company=company, channel="linkedin", persona="insider"),
        OutreachContact(name="Insider Two", role="PMM", company=company, channel="linkedin", persona="insider"),
        OutreachContact(name="Recruiter", role="Tech Recruiter", company=company, channel="email", email="recruiter@example.com", persona="recruiter"),
    ]
    messages = {c.name: f"Hi {c.name}, applying for {role} at {company}. Quick snapshot: shipped AI/IoT, $1M data assistant, Azure B2C. Could we do a quick 15-min screen?" for c in contacts}
    followups = {c.name: (datetime.utcnow() + timedelta(days=3)).isoformat() for c in contacts}
    plan = OutreachPlan(job_id=job_id, contacts=contacts, messages=messages, followups=followups)
    log_event({"type":"outreach_plan", "job_id": job_id, "contacts": [c.model_dump() for c in contacts]})
    return plan

@app.post("/followups/run")
def run_followups():
    # Stub: would read from sheet and create drafts/reminders; for now, just acknowledge.
    log_event({"type":"followups_run", "ts": datetime.utcnow().isoformat()})
    return {"ok": True, "scheduled": True}

@app.post("/summary/today")
def summary_today():
    # Stub: read TRACKER_PATH if exists and compute minimal numbers
    tracker = os.getenv("TRACKER_PATH")
    if tracker and os.path.exists(tracker):
        # Avoid heavy deps here; just say it's present
        msg = "Summary based on tracker present."
    else:
        msg = "Tracker not found; set TRACKER_PATH in .env."
    lines = [
        "Jobs found/applied: 3/2 (CompanyA PM, CompanyB TPM)",
        "Outreach: 5 sent (2 peers, 2 insiders, 1 recruiter)",
        "Responses: 1; Interviews: 1 scheduled",
        "Resume/skills: +1 bullet improved; A/B testing added to plan",
        "Misses/risks: Follow-up overdue for Recruiter X",
        "Top-3 tomorrow: Apply to Axon TPM; DM alum at Amazon; STAR for 'Dive Deep'"
    ]
    payload = {"message": msg, "digest": "\n".join(lines)}
    log_event({"type":"summary", "payload": payload})
    return payload
