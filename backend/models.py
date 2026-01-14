from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class Author(BaseModel):
    id: int
    full_name: str
    company: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    discovery_status: str
    created_at: Any

class Analysis(BaseModel):
    philosophy: Optional[str] = None
    principles: Optional[str] = None
    tone: Optional[str] = None
    beliefs: Optional[str] = None
    opportunities: Optional[str] = None

class PipelineStatus(BaseModel):
    discovered: bool
    pdf_uploaded: bool
    analyzed: bool
    email_generated: bool
    added_to_sheet: bool
    sent: bool

class AuthorDetail(Author):
    pipeline: Optional[PipelineStatus] = None
    analysis: Optional[Analysis] = None
    book_title: Optional[str] = None
    email_status: Optional[str] = None

class StatResponse(BaseModel):
    total_authors: int
    emails_sent_today: int
    pending_emails: int
    zoho_health: str
