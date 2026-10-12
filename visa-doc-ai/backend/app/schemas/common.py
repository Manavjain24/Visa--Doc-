from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class RequirementClassification(str, Enum):
    MANDATORY = "Mandatory"
    CONDITIONAL = "Conditional"
    RECOMMENDED = "Recommended"
    UNVERIFIED = "Unverified"
    NOT_APPLICABLE = "Not applicable"


class ClaimOutcome(str, Enum):
    SUPPORTED_BY_OFFICIAL = "Supported by official evidence"
    SUPPORTED_UNDER_CONDITIONS = "Supported only under specified conditions"
    NOT_ESTABLISHED = "Not established by sources reviewed"
    CONFLICTING_OFFICIAL = "Conflicting official information"
    UNABLE_TO_VERIFY = "Unable to verify"


class ResearchStatus(str, Enum):
    INITIALIZING = "initializing"
    PLANNING = "planning"
    SEARCHING = "searching"
    EXTRACTING = "extracting"
    VERIFYING = "verifying"
    EVALUATING = "evaluating"
    GENERATING_CHECKLIST = "generating_checklist"
    COMPLETED = "completed"
    FAILED = "failed"
    EXHAUSTED_BUDGET = "exhausted_budget"


class SourceTier(str, Enum):
    OFFICIAL = "official"  # .gov, .gc.ca, .gov.uk, official foreign ministries
    TRUSTED_PARTNER = "trusted_partner"  # VFS Global, TLScontact, BLS
    GENERAL = "general"  # blogs, travel sites, legal firms


def current_utc_time() -> datetime:
    return datetime.now(timezone.utc)
