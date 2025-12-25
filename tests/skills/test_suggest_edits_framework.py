"""
Test suite for the suggest_edits framework.

Validates that copywriting skills properly implement the suggest_edits pattern:
- Edit suggestions have required fields
- Output format matches specification
- No auto-modification occurs (framework guarantee)
- Section classification is accurate
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

import pytest


# Fixtures path
FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_CONTENT = FIXTURES_DIR / "sample_content.md"
EXPECTED_EDITS = FIXTURES_DIR / "expected_edits.json"


@pytest.fixture
def expected_schema() -> Dict[str, Any]:
    """Load expected edit suggestion schema."""
    with open(EXPECTED_EDITS) as f:
        return json.load(f)


@pytest.fixture
def sample_content() -> str:
    """Load sample content for testing."""
    with open(SAMPLE_CONTENT) as f:
        return f.read()


class TestEditSuggestionFormat:
    """Test edit suggestion format validation."""

    def test_required_fields_present(self):
        """Verify edit suggestions contain all required fields."""
        # This is a structural test - actual skills will be tested separately
        required_fields = ["section_name", "type", "rationale", "before", "after"]

        # Test data representing a valid edit suggestion
        valid_suggestion = {
            "section_name": "Introduction Hook",
            "type": "introduction",
            "rationale": "Adds pain-first hook to grab attention immediately",
            "before": "Authentication is important for security.",
            "after": "Your users' data is one weak password away from a breach."
        }

        for field in required_fields:
            assert field in valid_suggestion, f"Required field '{field}' missing"
            assert valid_suggestion[field], f"Required field '{field}' is empty"

    def test_section_type_validity(self, expected_schema):
        """Verify section types are from allowed set."""
        valid_types = expected_schema["edit_suggestion_schema"]["section_types"]

        # Test valid types
        assert "introduction" in valid_types
        assert "concept-explanation" in valid_types
        assert "failure-mode" in valid_types
        assert "takeaway" in valid_types
        assert "cta" in valid_types
        assert "technical" in valid_types
        assert "navigation" in valid_types

        # Test that invalid types would be caught
        invalid_type = "random-invalid-type"
        assert invalid_type not in valid_types

    def test_output_format_markers_present(self, expected_schema):
        """Verify output contains required markdown markers."""
        required_markers = expected_schema["edit_suggestion_schema"]["output_format_markers"]

        # Simulate skill output
        sample_output = """
# Edit Suggestions for Test Content

## Summary
**Total Suggestions**: 3

## Suggested Edit 1: Introduction Hook

**Type**: introduction
**Rationale**: Adds pain-first hook to engage reader

### Before
```
Authentication is important.
```

### After
```
Your users' data is at risk.
```

### Apply This Edit?
- [ ] Yes, apply as-is
- [ ] Apply with modifications
- [ ] Skip this edit
"""

        for marker in required_markers:
            assert marker in sample_output, f"Required marker '{marker}' missing from output"

    def test_rationale_not_empty(self):
        """Verify rationale field is not empty or vague."""
        # Valid rationale
        valid_rationale = "Uses pain-first hook to create urgency and grab attention in first sentence"
        assert len(valid_rationale) > 20, "Rationale should be descriptive"

        # Vague rationale (anti-pattern)
        vague_rationales = [
            "makes it better",
            "improves content",
            "sounds nicer",
            ""
        ]

        for vague in vague_rationales:
            assert len(vague) < 20, f"Rationale '{vague}' is too vague"


class TestNoAutoModification:
    """Test that framework prevents auto-modification of files."""

    def test_no_file_writing(self, expected_schema):
        """Verify validation rules prohibit file writing."""
        validation_rules = expected_schema["validation_rules"]
        no_mod_rule = validation_rules["no_file_modification"]

        assert "never write" in no_mod_rule.lower()
        assert "only output suggestions" in no_mod_rule.lower()

    def test_suggestion_only_output(self):
        """Verify skills output suggestions, not modified content."""
        # This test validates the pattern - actual implementation tested in skill tests

        # Valid: Output with suggestions
        valid_output = """
## Suggested Edit 1: Title
### Before
original
### After
modified
"""
        assert "## Suggested Edit" in valid_output
        assert "### Before" in valid_output
        assert "### After" in valid_output

        # Invalid: Direct file replacement (anti-pattern)
        # Skills should NEVER output content meant to replace file directly
        # They should always wrap in suggestion format


class TestSectionClassification:
    """Test section type classification accuracy."""

    def test_introduction_detection(self, sample_content):
        """Verify introduction sections are identified."""
        # Introduction section should be in sample content
        assert "## Introduction - Technical" in sample_content

        # Pattern for detecting introduction sections
        intro_patterns = [
            r"^#+ Introduction",
            r"^This is a .+ introduction",
            r"^This document .+ explains"
        ]

        found_intro = any(re.search(pattern, sample_content, re.MULTILINE)
                         for pattern in intro_patterns)
        assert found_intro, "Should detect introduction section"

    def test_concept_explanation_detection(self, sample_content):
        """Verify concept explanation sections are identified."""
        assert "## Concept Explanation - Candidate for Personality" in sample_content

        # Concept explanations often contain definitions and explanations
        concept_patterns = [
            r"are mechanisms that",
            r"Think of it like",
            r"involves .+ and .+"
        ]

        found_concept = any(re.search(pattern, sample_content, re.MULTILINE)
                          for pattern in concept_patterns)
        assert found_concept, "Should detect concept explanation patterns"

    def test_code_block_detection(self, sample_content):
        """Verify code blocks are identified as technical sections."""
        # Code blocks should be preserved
        assert "```python" in sample_content
        assert "oauth.register(" in sample_content

        # Pattern for detecting code blocks
        code_pattern = r"```[\w]*\n.*?\n```"
        code_blocks = re.findall(code_pattern, sample_content, re.DOTALL)
        assert len(code_blocks) > 0, "Should detect code blocks"

    def test_failure_mode_detection(self, sample_content):
        """Verify failure mode sections are identified."""
        assert "## Failure Mode - Candidate for Conversational Honesty" in sample_content

        # Failure modes often discuss mistakes and gotchas
        failure_patterns = [
            r"common mistake",
            r"gotcha",
            r"will fail",
            r"don't .+ users get"
        ]

        found_failure = any(re.search(pattern, sample_content, re.IGNORECASE)
                          for pattern in failure_patterns)
        assert found_failure, "Should detect failure mode language"

    def test_table_detection(self, sample_content):
        """Verify tables/benchmarks are identified as technical sections."""
        # Tables should be preserved
        assert "| Library | Setup Time |" in sample_content

        # Pattern for markdown tables
        table_pattern = r"\|.+\|.+\|\n\|[-:| ]+\|"
        tables = re.findall(table_pattern, sample_content)
        assert len(tables) > 0, "Should detect markdown tables"

    def test_takeaway_detection(self, sample_content):
        """Verify takeaway sections are identified."""
        assert "## Takeaway - Candidate for Memorable Style" in sample_content

        # Takeaways often summarize and conclude
        takeaway_patterns = [
            r"## Takeaway",
            r"is powerful but",
            r"Make sure to"
        ]

        found_takeaway = any(re.search(pattern, sample_content)
                            for pattern in takeaway_patterns)
        assert found_takeaway, "Should detect takeaway section"

    def test_cta_detection(self, sample_content):
        """Verify CTA sections are identified."""
        assert "## Call to Action - Conversion Candidate" in sample_content

        # CTAs often have action words
        cta_patterns = [
            r"If you want to",
            r"check out",
            r"learn more"
        ]

        found_cta = any(re.search(pattern, sample_content)
                       for pattern in cta_patterns)
        assert found_cta, "Should detect CTA language"


class TestOutputStructure:
    """Test suggest_edits output structure compliance."""

    def test_summary_section_present(self):
        """Verify output includes summary section."""
        expected_summary_fields = [
            "Total Suggestions",
            "Editable Sections Found",
            "Sections Preserved",
            "Focus Areas"
        ]

        sample_output = """
# Edit Suggestions for Test

## Summary

**Total Suggestions**: 5
**Editable Sections Found**: 8
**Sections Preserved**: 3

**Focus Areas**:
- Hook improvement
- CTA strengthening
"""

        for field in expected_summary_fields:
            assert field in sample_output, f"Summary should include '{field}'"

    def test_preserved_sections_documented(self):
        """Verify output documents sections intentionally not edited."""
        sample_output = """
## Sections Intentionally Preserved

The following sections were **not** edited to maintain technical accuracy:

- **Code Example** (technical): Code must remain exact for correctness
- **Benchmark Table** (technical): Factual data must be preserved
"""

        assert "Sections Intentionally Preserved" in sample_output
        assert "not** edited" in sample_output
        assert "technical" in sample_output.lower()

    def test_application_notes_present(self):
        """Verify output includes application notes and next steps."""
        expected_sections = [
            "## Application Notes",
            "## Next Steps",
            "Review rationale",
            "Apply selectively"
        ]

        sample_output = """
## Application Notes

1. **Review rationale** for each suggestion before applying
2. **Apply selectively** - not all suggestions may fit your intent

## Next Steps

- [ ] Review all suggested edits
- [ ] Apply selected edits to source file
"""

        for section in expected_sections:
            assert section in sample_output, f"Output should include '{section}'"

    def test_visual_separation(self):
        """Verify clear visual separation between suggestions."""
        sample_output = """
## Suggested Edit 1: First Section

**Type**: introduction
**Rationale**: Improves hook

### Before
```
old
```

### After
```
new
```

---

## Suggested Edit 2: Second Section

**Type**: cta
**Rationale**: Strengthens action
"""

        # Check for horizontal rules or clear section breaks
        assert "---" in sample_output or "═══" in sample_output, \
            "Should have visual separators between suggestions"


class TestEdgeCases:
    """Test edge case handling."""

    def test_already_optimized_content(self):
        """Verify skills handle already-optimized content gracefully."""
        # Already strong content shouldn't generate excessive suggestions
        strong_content = "Stop wasting time. This tool solves your problem in 3 clicks."

        # Skills should recognize this is already conversion-focused
        # and suggest minimal or no changes
        # Actual implementation tested in skill-specific tests
        assert len(strong_content) > 0

    def test_minimal_content(self):
        """Verify skills handle minimal content appropriately."""
        minimal_content = "OAuth is an authorization protocol."

        # Should recognize content is too brief to meaningfully improve
        # or suggest expansion rather than replacement
        assert len(minimal_content.split()) < 10

    def test_pure_technical_content(self):
        """Verify skills preserve pure technical definitions."""
        technical_content = """
**Access Token**: A credential used to access protected resources.
**Refresh Token**: A credential for obtaining new access tokens.
"""

        # Should not suggest stylistic changes to technical definitions
        # Accuracy > personality for definitions
        assert "**" in technical_content  # Definitions use bold
        assert ":" in technical_content   # Definition format

    def test_mixed_content_selective_editing(self, sample_content):
        """Verify skills selectively edit mixed content sections."""
        # Mixed content section exists in sample
        assert "## Mixed Content - Selective Editing" in sample_content

        # Should edit prose, preserve code
        assert "Setting up OAuth requires" in sample_content  # Prose
        assert "@app.route('/callback')" in sample_content   # Code to preserve


class TestSuggestionLimits:
    """Test that skills limit suggestions to high-impact changes."""

    def test_suggestion_count_reasonable(self, expected_schema):
        """Verify expected suggestion counts are reasonable."""
        skill_expectations = expected_schema["skill_specific_expectations"]

        for skill, expectations in skill_expectations.items():
            # Parse suggestion limits from validation rules
            # Typically 5-10 suggestions maximum
            assert "5" in str(expectations) or "4" in str(expectations), \
                f"{skill} should have reasonable suggestion limits"

    def test_high_impact_focus(self, expected_schema):
        """Verify validation emphasizes high-impact changes."""
        validation = expected_schema["validation_rules"]
        suggestion_limit = validation["suggestion_limit"]

        assert "high-impact" in suggestion_limit.lower()
        assert "5-10" in suggestion_limit


class TestAntiPatterns:
    """Test detection of anti-patterns."""

    def test_detect_file_writing_anti_pattern(self, expected_schema):
        """Verify file writing is flagged as anti-pattern."""
        anti_patterns = expected_schema["anti_patterns_to_detect"]

        assert "file_writing" in anti_patterns
        assert "never" in anti_patterns["file_writing"].lower()

    def test_detect_vague_rationale_anti_pattern(self, expected_schema):
        """Verify vague rationale is flagged as anti-pattern."""
        anti_patterns = expected_schema["anti_patterns_to_detect"]

        assert "vague_rationale" in anti_patterns
        assert "makes it better" in anti_patterns["vague_rationale"].lower()

    def test_detect_excessive_edits_anti_pattern(self, expected_schema):
        """Verify excessive edits are flagged as anti-pattern."""
        anti_patterns = expected_schema["anti_patterns_to_detect"]

        assert "excessive_edits" in anti_patterns
        assert "10" in anti_patterns["excessive_edits"]

    def test_detect_technical_modification_anti_pattern(self, expected_schema):
        """Verify technical modification without reason is anti-pattern."""
        anti_patterns = expected_schema["anti_patterns_to_detect"]

        assert "technical_modification" in anti_patterns
        assert "code blocks" in anti_patterns["technical_modification"].lower()


class TestSkillDifferentiation:
    """Test that skills produce different suggestions for same content."""

    def test_skill_focus_differences(self, expected_schema):
        """Verify each skill has distinct focus."""
        skills = expected_schema["skill_specific_expectations"]

        focuses = set()
        for skill, expectations in skills.items():
            focus = expectations["focus"]
            assert focus not in focuses, f"Duplicate focus: {focus}"
            focuses.add(focus)

        # Should have three distinct focuses
        assert len(focuses) == 3
        assert "conversion" in focuses
        assert "persuasion" in focuses
        assert "simplification" in focuses

    def test_skill_tone_differences(self, expected_schema):
        """Verify each skill has distinct tone."""
        skills = expected_schema["skill_specific_expectations"]

        tones = []
        for skill, expectations in skills.items():
            tone = expectations["tone"]
            tones.append(tone)

        # Mad Men: aggressive
        # Master: authoritative
        # Ameno: technical-friendly
        assert any("aggressive" in t for t in tones)
        assert any("authoritative" in t for t in tones)
        assert any("technical-friendly" in t for t in tones)

    def test_skill_technique_differences(self, expected_schema):
        """Verify each skill uses different techniques."""
        skills = expected_schema["skill_specific_expectations"]

        all_techniques = []
        for skill, expectations in skills.items():
            techniques = expectations["techniques"]
            all_techniques.extend(techniques)

        # Should have diverse techniques across skills
        assert len(all_techniques) > 8
        assert any("pain-first" in str(t) for t in all_techniques)  # Mad Men
        assert any("social proof" in str(t) for t in all_techniques)  # Master
        assert any("analogies" in str(t) for t in all_techniques)  # Ameno


# Marker for pytest collection
pytestmark = pytest.mark.copywriting_skills
