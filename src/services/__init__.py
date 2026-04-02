# Pipeline Services
# Wrapper layer for external dependencies (narrative-scorer, etc.)

from .narrative_scorer_wrapper import score_narrative, NarrativeScorerService
from .remem_event_segmenter import EventSegmenter, segment_narrative, EventSegment

__all__ = [
    'score_narrative',
    'NarrativeScorerService',
    'EventSegmenter',
    'segment_narrative',
    'EventSegment',
]
