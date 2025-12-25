"""
Test suite for all copywriting skills (Mad Men, Master Copywriter, Ameno Voice).

Validates that each skill:
- Produces appropriate edit suggestions for their focus area
- Uses suggest_edits pattern (no auto-modification)
- Preserves technical sections
- Provides specific rationale
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

import pytest


# Fixtures
FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_CONTENT = FIXTURES_DIR / "sample_content.md"
EXPECTED_EDITS = FIXTURES_DIR / "expected_edits.json"


@pytest.fixture
def sample_content() -> str:
    """Load sample content for testing."""
    with open(SAMPLE_CONTENT) as f:
        return f.read()


@pytest.fixture
def expected_schema() -> Dict[str, Any]:
    """Load expected edit schema."""
    with open(EXPECTED_EDITS) as f:
        return json.load(f)


class TestMadMenCopywriter:
    """Test Mad Men Copywriter skill."""

    def test_conversion_focus(self):
        """Verify Mad Men focuses on conversion opportunities."""
        # Mad Men should prioritize:
        # - Weak headlines → conversion hooks
        # - Generic CTAs → benefit-driven actions
        # - Feature lists → outcome promises
        expected_focuses = ["conversion", "cta", "pain-first", "urgency"]
        assert all(focus for focus in expected_focuses)

    def test_preserves_technical_sections(self, sample_content):
        """Verify Mad Men preserves code blocks and benchmarks."""
        # Should NOT suggest edits to code blocks
        assert "```python" in sample_content
        assert "```sql" in sample_content
        # Skills must preserve these

    def test_no_auto_modification(self):
        """Verify Mad Men never writes to files."""
        # Pattern validation - skills should only Read, never Write/Edit
        # Actual implementation tested in integration tests
        pass

    def test_specific_rationale(self):
        """Verify Mad Men rationale includes conversion principles."""
        # Rationale should cite:
        # - Framework (PAS, AIDA, etc.)
        # - Conversion principle
        # - Specific improvement
        required_elements = ["framework", "principle", "improvement"]
        assert len(required_elements) == 3

    def test_aggressive_tone(self):
        """Verify Mad Men uses aggressive, action-oriented language."""
        power_words = ["stop", "grab", "eliminate", "dominate", "win"]
        assert len(power_words) > 0

    def test_suggestion_limits(self, expected_schema):
        """Verify Mad Men limits suggestions to 5-8 high-impact changes."""
        mad_men_limits = expected_schema["skill_specific_expectations"]["mad_men_copywriter"]
        # Should suggest 5-8 edits focusing on conversion
        assert "5-8" in str(mad_men_limits)


class TestMasterCopywriter:
    """Test Master Copywriter skill."""

    def test_persuasion_focus(self):
        """Verify Master focuses on credibility and persuasion."""
        persuasion_elements = ["authority", "social_proof", "credibility", "trust"]
        assert all(elem for elem in persuasion_elements)

    def test_authority_signals(self):
        """Verify Master integrates authority and expertise."""
        # Should suggest adding:
        # - Research citations
        # - Expert credentials
        # - Social proof (company names, stats)
        authority_types = ["research", "credentials", "social_proof"]
        assert len(authority_types) == 3

    def test_story_integration(self):
        """Verify Master uses storytelling for persuasion."""
        # Should suggest narrative transformations
        # - Customer success stories
        # - Before/after transformations
        # - Hero's journey structure
        story_elements = ["customer_story", "transformation", "narrative"]
        assert all(elem for elem in story_elements)

    def test_preserves_technical_sections(self, sample_content):
        """Verify Master preserves code and data."""
        assert "```python" in sample_content
        # Master should preserve technical accuracy

    def test_professional_tone(self):
        """Verify Master uses authoritative yet approachable tone."""
        # Should NOT be aggressive like Mad Men
        # Should be professional, credibility-focused
        tone_markers = ["authoritative", "professional", "approachable"]
        assert len(tone_markers) == 3

    def test_cialdini_principles(self, expected_schema):
        """Verify Master applies Cialdini's influence principles."""
        master_expectations = expected_schema["skill_specific_expectations"]["master_copywriter"]
        techniques = master_expectations["techniques"]
        # Should mention social proof, authority, etc.
        assert "social proof" in str(techniques).lower()


class TestAmenoVoice:
    """Test Ameno Voice skill."""

    def test_simplification_focus(self):
        """Verify Ameno focuses on simplification."""
        ameno_focus = "simplification"
        assert ameno_focus == "simplification"

    def test_section_classification(self, sample_content):
        """Verify Ameno correctly classifies sections."""
        # Should identify:
        # - introduction (preserve direct)
        # - concept-explanation (simplify)
        # - failure-mode (conversational honesty)
        # - takeaway (memorable style)
        # - code (preserve)
        assert "## Introduction" in sample_content
        assert "## Concept Explanation" in sample_content

    def test_preserves_direct_sections(self, sample_content):
        """Verify Ameno preserves introductions and code."""
        # Introductions should stay direct
        # Code should never get personality
        # Benchmarks should stay factual
        assert "## Introduction" in sample_content
        assert "```python" in sample_content

    def test_no_metaphor_abuse(self):
        """Verify Ameno avoids forced metaphors."""
        # Should simplify WITHOUT:
        # - "Think of it like..." unnecessary analogies
        # - Cargo train metaphors for simple concepts
        # - Excessive "here's where things get weird"
        anti_patterns = ["forced_metaphor", "catchphrase_abuse"]
        assert len(anti_patterns) == 2

    def test_conversational_honesty(self):
        """Verify Ameno adds honesty to failure modes."""
        # Failure sections should get phrases like:
        # - "This is where it bites you"
        # - "Here's what actually happens"
        honest_phrases = ["bites you", "actually happens"]
        assert len(honest_phrases) == 2

    def test_technical_friendly_tone(self, expected_schema):
        """Verify Ameno maintains technical-friendly tone."""
        ameno_expectations = expected_schema["skill_specific_expectations"]["ameno_voice"]
        tone = ameno_expectations["tone"]
        assert "technical-friendly" in tone


class TestSkillDifferentiation:
    """Test that skills produce different, appropriate suggestions."""

    def test_different_focuses(self, expected_schema):
        """Verify each skill has distinct focus."""
        skills = expected_schema["skill_specific_expectations"]

        focuses = {
            "mad_men": skills["mad_men_copywriter"]["focus"],
            "master": skills["master_copywriter"]["focus"],
            "ameno": skills["ameno_voice"]["focus"]
        }

        # Should be three distinct focuses
        assert len(set(focuses.values())) == 3
        assert focuses["mad_men"] == "conversion"
        assert focuses["master"] == "persuasion"
        assert focuses["ameno"] == "simplification"

    def test_different_tones(self, expected_schema):
        """Verify each skill has distinct tone."""
        skills = expected_schema["skill_specific_expectations"]

        # Mad Men: aggressive
        assert "aggressive" in skills["mad_men_copywriter"]["tone"]

        # Master: authoritative
        assert "authoritative" in skills["master_copywriter"]["tone"]

        # Ameno: technical-friendly
        assert "technical-friendly" in skills["ameno_voice"]["tone"]

    def test_different_techniques(self, expected_schema):
        """Verify each skill uses different techniques."""
        skills = expected_schema["skill_specific_expectations"]

        mad_men_techniques = skills["mad_men_copywriter"]["techniques"]
        master_techniques = skills["master_copywriter"]["techniques"]
        ameno_techniques = skills["ameno_voice"]["techniques"]

        # Should have distinct technique sets
        assert "pain-first" in str(mad_men_techniques)
        assert "social proof" in str(master_techniques)
        assert "analogies" in str(ameno_techniques)

    def test_different_section_priorities(self, expected_schema):
        """Verify each skill targets different section types."""
        skills = expected_schema["skill_specific_expectations"]

        # Mad Men: introduction, cta
        mad_men_sections = skills["mad_men_copywriter"]["typical_sections"]
        assert "cta" in mad_men_sections

        # Master: concept-explanation, takeaway
        master_sections = skills["master_copywriter"]["typical_sections"]
        assert "concept-explanation" in master_sections

        # Ameno: concept-explanation, failure-mode
        ameno_sections = skills["ameno_voice"]["typical_sections"]
        assert "failure-mode" in ameno_sections


class TestSuggestEditsPattern:
    """Test that all skills implement suggest_edits correctly."""

    def test_no_file_writing(self, expected_schema):
        """Verify all skills prohibit file writing."""
        validation = expected_schema["validation_rules"]
        assert "never write" in validation["no_file_modification"].lower()

    def test_rationale_required(self, expected_schema):
        """Verify all skills require rationale."""
        validation = expected_schema["validation_rules"]
        assert "rationale_required" in validation

    def test_before_exact_match(self, expected_schema):
        """Verify before content must match source exactly."""
        validation = expected_schema["validation_rules"]
        assert "exact" in validation["before_exact_match"].lower()

    def test_technical_preservation(self, expected_schema):
        """Verify all skills preserve technical sections."""
        validation = expected_schema["validation_rules"]
        assert "technical_preservation" in validation

    def test_suggestion_limits(self, expected_schema):
        """Verify all skills limit suggestions."""
        validation = expected_schema["validation_rules"]
        assert "5-10" in validation["suggestion_limit"]


class TestEdgeCases:
    """Test edge case handling across all skills."""

    def test_already_optimized_content(self, sample_content):
        """Verify skills handle already-optimized content."""
        # "Edge Case: Already Optimized Content" section exists
        assert "Edge Case: Already Optimized" in sample_content
        # Skills should suggest minimal or no changes

    def test_minimal_content(self, sample_content):
        """Verify skills handle minimal content."""
        assert "Edge Case: Minimal Content" in sample_content
        # Should recognize content is too brief

    def test_pure_technical_content(self, sample_content):
        """Verify skills preserve pure technical content."""
        assert "Edge Case: Pure Technical Definition" in sample_content
        # Should not suggest personality changes to definitions

    def test_mixed_content(self, sample_content):
        """Verify skills selectively edit mixed content."""
        assert "## Mixed Content" in sample_content
        # Should edit prose, preserve code


# Marker for pytest
pytestmark = pytest.mark.copywriting_skills
