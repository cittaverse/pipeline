#!/usr/bin/env python3
"""
Narrative Scorer Wrapper for Pipeline Services

This wrapper provides a stable API for pipeline services,
absorbing any breaking changes in the narrative-scorer library.

Version: 1.0.0 (Phase 1 - Skeleton)
Compatibility: narrative-scorer>=0.7.0,<0.8.0

Status: SKELETON — Implementation pending DASHSCOPE_API_KEY validation
"""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


# Import from narrative-scorer library (pending v0.7.0 release)
try:
    from narrative_scorer import score_narrative as _score_narrative
    from narrative_scorer import LLMFeatureExtractor, LLMConfig
    LIBRARY_AVAILABLE = True
    logger.info("narrative-scorer library imported successfully")
except ImportError as e:
    logger.warning(f"narrative-scorer library not available: {e}")
    logger.info("Falling back to local narrative_scorer_v0.4.py implementation")
    LIBRARY_AVAILABLE = False


def score_narrative(text: str, use_llm: bool = True, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Score a single narrative (wrapper for library function).
    
    Args:
        text: The narrative text to score
        use_llm: Whether to use LLM-enhanced scoring (default: True)
        api_key: Optional DashScope API key (falls back to env var if not provided)
    
    Returns:
        Dictionary with scores and metadata:
        {
            'composite_score': float,
            'event_richness': float,
            'temporal_causal_coherence': float,
            'emotional_depth': float,
            'identity_integration': float,
            'information_density': float,
            'narrative_coherence': float,
            'metadata': dict,
        }
    
    Raises:
        ImportError: If narrative-scorer library is not installed
        Exception: If scoring fails (with graceful fallback logging)
    
    Status: SKELETON — Implementation pending v0.7.0 release
    """
    if not LIBRARY_AVAILABLE:
        # TODO: Implement fallback to local narrative_scorer_v0.4.py
        raise ImportError(
            "narrative-scorer library is required. "
            "Install with: pip install narrative-scorer>=0.7.0,<0.8.0\n"
            "Note: Local fallback (narrative_scorer_v0.4.py) available but not yet integrated."
        )
    
    try:
        return _score_narrative(text, use_llm=use_llm, api_key=api_key)
    except Exception as e:
        logger.error(f"Narrative scoring failed: {e}")
        raise


class NarrativeScorerService:
    """
    Service layer for narrative scoring (used by pipeline APIs).
    
    This service class provides:
    - Configuration management (LLM on/off, API key handling)
    - Logging and monitoring hooks
    - Batch scoring support
    - Error handling and fallback behavior
    
    Usage:
        scorer = NarrativeScorerService(use_llm=True)
        result = scorer.score("今天天气很好...")
        print(result['composite_score'])
    
    Status: SKELETON — Implementation pending v0.7.0 release
    """
    
    def __init__(
        self,
        use_llm: bool = True,
        api_key: Optional[str] = None,
        fallback_to_rule_only: bool = True,
    ):
        """
        Initialize the narrative scorer service.
        
        Args:
            use_llm: Enable LLM-enhanced scoring (default: True)
            api_key: DashScope API key (optional, falls back to env var)
            fallback_to_rule_only: Fall back to rule-only if LLM fails (default: True)
        """
        self.use_llm = use_llm
        self.api_key = api_key
        self.fallback_to_rule_only = fallback_to_rule_only
        
        if use_llm and LIBRARY_AVAILABLE:
            config = LLMConfig(
                api_key=api_key,
                fallback_to_rule_only=fallback_to_rule_only,
            )
            self.extractor = LLMFeatureExtractor(config)
            logger.info("NarrativeScorerService initialized with LLM enhancement")
        else:
            self.extractor = None
            logger.info(
                f"NarrativeScorerService initialized (rule-only): "
                f"use_llm={use_llm}, library_available={LIBRARY_AVAILABLE}"
            )
    
    def score(self, text: str) -> Dict[str, Any]:
        """
        Score a narrative.
        
        Args:
            text: The narrative text to score
        
        Returns:
            Dictionary with scores and metadata (see score_narrative)
        
        Status: SKELETON — Implementation pending v0.7.0 release
        """
        return score_narrative(text, use_llm=self.use_llm, api_key=self.api_key)
    
    def score_batch(self, texts: list[str]) -> list[Dict[str, Any]]:
        """
        Score multiple narratives in batch.
        
        Args:
            texts: List of narrative texts to score
        
        Returns:
            List of score dictionaries (same order as input)
        
        Status: SKELETON — Implementation pending v0.7.0 release
        """
        results = []
        for i, text in enumerate(texts):
            try:
                result = self.score(text)
                results.append(result)
                logger.debug(f"Batch score {i+1}/{len(texts)}: OK")
            except Exception as e:
                logger.error(f"Batch score {i+1}/{len(texts)} failed: {e}")
                results.append({'error': str(e), 'index': i})
        return results


# TODO: Phase 1 Implementation Checklist
# [ ] Integrate narrative-scorer v0.7.0 from PyPI
# [ ] Implement fallback to local narrative_scorer_v0.4.py (for offline/development)
# [ ] Add batch scoring with async support
# [ ] Add caching layer (Redis/memory) for repeated narratives
# [ ] Add monitoring hooks (latency, error rate, cost tracking)
# [ ] Write unit tests (mocked LLM)
# [ ] Write integration tests (live LLM, pending API key)
# [ ] Update pipeline README with wrapper usage examples
