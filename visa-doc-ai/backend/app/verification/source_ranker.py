from typing import List
from app.schemas.source import RetrievedSource
from app.schemas.common import SourceTier
from app.utils.url_utils import is_official_domain, get_source_tier


class SourceRanker:
    """Ranks and prioritizes sources according to evidentiary authority."""

    @staticmethod
    def get_source_weight(source: RetrievedSource) -> float:
        tier = source.metadata.tier
        if tier == SourceTier.OFFICIAL or source.metadata.is_official:
            return 1.0
        elif tier == SourceTier.TRUSTED_PARTNER:
            return 0.85
        return 0.4

    @staticmethod
    def rank_sources(sources: List[RetrievedSource]) -> List[RetrievedSource]:
        """Ranks sources with accessible official sources first."""
        return sorted(
            sources,
            key=lambda s: (
                s.is_accessible,
                SourceRanker.get_source_weight(s),
                s.metadata.http_status == 200
            ),
            reverse=True
        )
