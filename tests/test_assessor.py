"""
Tests for Narrative Assessor
"""

import pytest
from src.assessor import NarrativeAssessor, AssessmentResult


class TestNarrativeAssessor:
    """叙事评估器测试"""
    
    @pytest.fixture
    def assessor(self):
        """创建测试用评估器"""
        return NarrativeAssessor(model="qwen-plus", language="zh-CN")
    
    @pytest.fixture
    def sample_text(self):
        """示例叙事文本"""
        return """
        那是我年轻时候的事情了，大概是 1978 年吧，那时候我还在纺织厂工作。
        每天早上五点半就要起床，先给一家老小做饭。那时候条件苦啊，但是大家都很有干劲。
        我记得特别清楚，厂里有一台老式织布机，声音特别大，轰隆轰隆的。
        有一次，我连续工作了 36 个小时，因为赶一批出口订单。
        """
    
    def test_init(self, assessor):
        """测试初始化"""
        assert assessor.model == "qwen-plus"
        assert assessor.language == "zh-CN"
    
    def test_assess_text(self, assessor, sample_text):
        """测试文本评估"""
        result = assessor.assess_text(sample_text)
        
        assert isinstance(result, AssessmentResult)
        assert 0 <= result.overall_score <= 100
        assert result.word_count > 0
        assert result.event_count >= 0
    
    def test_batch_assess(self, assessor, sample_text):
        """测试批量评估"""
        texts = [sample_text, sample_text]
        results = assessor.batch_assess(texts)
        
        assert len(results) == 2
        for result in results:
            assert isinstance(result, AssessmentResult)
    
    def test_score_ranges(self, assessor, sample_text):
        """测试评分范围"""
        result = assessor.assess_text(sample_text)
        
        assert 0 <= result.internal_details_score <= 100
        assert 0 <= result.external_details_score <= 100
        assert 0 <= result.event_segmentation_score <= 100
        assert 0 <= result.coherence_score <= 100
        assert 0 <= result.overall_score <= 100


class TestAssessmentResult:
    """评估结果数据结构测试"""
    
    def test_result_creation(self):
        """测试结果创建"""
        result = AssessmentResult(
            internal_details_score=68.0,
            external_details_score=45.0,
            event_segmentation_score=72.0,
            coherence_score=78.0,
            overall_score=66.0,
            word_count=312,
            event_count=4,
            insights=["建议鼓励更多感官细节描述"],
            evidence={"internal_details": ["1978 年", "纺织厂"]}
        )
        
        assert result.internal_details_score == 68.0
        assert result.overall_score == 66.0
        assert len(result.insights) == 1
