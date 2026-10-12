import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from app.schemas.common import SourceTier

OFFICIAL_GOV_DOMAINS = [
    # US
    "state.gov", "travel.state.gov", "uscis.gov", "dhs.gov",
    # UK
    "gov.uk", "ukvi.homeoffice.gov.uk",
    # Canada
    "canada.ca", "cic.gc.ca", "gc.ca",
    # Schengen / Europe
    "auswaertiges-amt.de", "germany.info", "diplo.de", "bmi.bund.de",
    "diplomatie.gouv.fr", "france-visas.gouv.fr",
    "esteri.it", "schengenvisainfo.com",
    "ind.nl", "government.nl",
    "migrationsverket.se",
    "udi.no",
    "migri.fi",
    "mae.ro", "mfa.gov.tr", "mfa.gr",
    # Australia & NZ
    "homeaffairs.gov.au", "immigration.govt.nz",
    # Asia
    "mofa.go.jp", "visa.go.kr", "ica.gov.sg", "mea.gov.in"
]

TRUSTED_PARTNER_DOMAINS = [
    "vfsglobal.com",
    "tlscontact.com",
    "blsinternational.com",
    "cibtvisas.com"
]


def extract_domain(url: str) -> str:
    """Extract lowercase netloc without port."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if ":" in domain:
        domain = domain.split(":")[0]
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def is_official_domain(url: str) -> bool:
    """Checks if a domain belongs to a government or embassy."""
    domain = extract_domain(url)
    
    # Check general gov TLD patterns
    if domain.endswith(".gov") or ".gov." in domain:
        return True
    if domain.endswith(".gc.ca") or domain.endswith(".gouv.fr"):
        return True
    if domain.endswith(".bund.de") or domain.endswith(".diplo.de"):
        return True
        
    for official in OFFICIAL_GOV_DOMAINS:
        if domain == official or domain.endswith("." + official):
            return True
            
    return False


def get_source_tier(url: str) -> SourceTier:
    """Determines the trust tier of the source URL."""
    if is_official_domain(url):
        return SourceTier.OFFICIAL
    
    domain = extract_domain(url)
    for trusted in TRUSTED_PARTNER_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return SourceTier.TRUSTED_PARTNER
            
    return SourceTier.GENERAL


def normalize_url(url: str) -> str:
    """Normalizes URL by stripping query tracking params and fragments."""
    try:
        parsed = urlparse(url)
        # Strip tracking query params
        tracking_params = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "ref", "fbclid"}
        q_params = [
            (k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=False)
            if k.lower() not in tracking_params
        ]
        new_query = urlencode(q_params)
        normalized = urlunparse((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip('/') if parsed.path != '/' else '/',
            '',
            new_query,
            ''  # strip fragments
        ))
        return normalized
    except Exception:
        return url.strip()
