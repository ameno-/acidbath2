# DataCard Style Library

Style templates for datacard assets—metric and statistic visualization cards. DataCards are square or portrait (1200x1200 or 1200x1600 pixels) emphasizing bold numbers and data with dramatic visual impact.

---

## CRITICAL: DataCard Nano Banana Guidelines

⚠️ **NUMBERS ARE SAFER THAN WORDS**

1. **BOLD NUMBERS** - Large metrics are the hero (95%, 36x, $4.2K)
2. **MINIMAL SUPPORTING TEXT** - 0-2 words beyond the number
3. **DRAMATIC LIGHTING** - Theatrical spotlight, high contrast
4. **COLOR CODING** - Green=success, Orange=warning, Cyan=neutral
5. **SQUARE/PORTRAIT FORMAT** - 1:1 or 3:4 aspect ratio

---

## Style 1: Metric Hero

### Description
Single impressive number/percentage with dramatic lighting. The number is the star—large, bold, glowing. Perfect for highlighting single metrics.

### Nano Banana Prompt Template

```
Bold metric visualization with dramatic lighting on dark background. Number is hero of composition.

Central element: "[METRIC_VALUE]" rendered huge (60-70% of frame) in bold sans-serif. [NUMBER_COLOR] neon glow with strong bloom.

Background: Pure black or deep charcoal with dramatic spotlight.

Lighting: Theatrical spotlight from [LIGHT_DIRECTION] creating rim lighting. Strong [NUMBER_COLOR] glow. Volumetric light rays optional.

Optional context: "[METRIC_CONTEXT]" in smaller text (1 word: "FASTER", "SAVED", "IMPROVED"). Position below or beside metric.

Aesthetic: Bold, confident, data-driven.

Technical specifications: [DIMENSIONS] (1200x1200 or 1200x1600), square or portrait aspect ratio.
```

### Placeholder Variables
- `[METRIC_VALUE]`: "95%", "36x", "$4.2K", "10K", "2.5s"
- `[NUMBER_COLOR]`: Green (#4caf50) for success, Cyan (#00ffff) neutral, Orange (#ff6600) warning
- `[LIGHT_DIRECTION]`: upper-left, behind, upper-right
- `[METRIC_CONTEXT]`: "FASTER", "SAVED", "REDUCED", "IMPROVED"
- `[DIMENSIONS]`: 1200x1200 or 1200x1600

---

## Style 2: Comparison Card

### Description
Two metrics side-by-side showing before/after or A vs B comparison. Visual contrast emphasizes the difference.

### Nano Banana Prompt Template

```
Split-screen comparison card showing two metrics with visual contrast. Dark background.

Left side: "[METRIC_A]" in [COLOR_A] (e.g., "3 hours" in orange suggesting problem)
Right side: "[METRIC_B]" in [COLOR_B] (e.g., "5 min" in green suggesting solution)

Visual split: Vertical line or gradient transition separating left/right. Color zones reinforce contrast.

Lighting: Each side lit with its respective color. Dramatic contrast between sides.

Optional labels: "[LABEL_A]" and "[LABEL_B]" (1 word each: "BEFORE", "AFTER" or "OLD", "NEW")

Aesthetic: Clear comparison, visual contrast emphasizes improvement or difference.

Technical specifications: [DIMENSIONS], square or portrait aspect ratio.
```

### Placeholder Variables
- `[METRIC_A/B]`: Before/after values or comparison values
- `[COLOR_A]`: Orange/red for problem state
- `[COLOR_B]`: Green/cyan for solution state
- `[LABEL_A/B]`: "BEFORE"/"AFTER", "OLD"/"NEW", "SLOW"/"FAST"
- `[DIMENSIONS]`: 1200x1200 or 1200x1600

---

## Style 3: Progress Indicator

### Description
Visual representation of progress, improvement, or completion. Abstract bar, gauge, or fill showing advancement.

### Nano Banana Prompt Template

```
Progress visualization showing [PROGRESS_CONCEPT] through abstract fill or bar. Dark background.

Visual element: [PROGRESS_VISUAL] showing [PERCENTAGE]% completion/improvement. Can be:
- Horizontal bar filling from left (0%) to [PERCENTAGE]% with glow
- Circular gauge/arc filling to [PERCENTAGE]%
- Container filling from bottom to [PERCENTAGE]% height

Progress area: [FILL_COLOR] glow (green for success, cyan for neutral)
Empty area: Dark/dim

Optional metric: "[PERCENTAGE]%" displayed prominently

Lighting: [FILL_COLOR] glow from filled area. Dramatic light emphasizing progress.

Aesthetic: Achievement, progression, completion.

Technical specifications: [DIMENSIONS], square or portrait aspect ratio.
```

### Placeholder Variables
- `[PROGRESS_CONCEPT]`: "optimization progress", "cost reduction", "improvement"
- `[PROGRESS_VISUAL]`: "horizontal bar", "circular gauge", "vertical container"
- `[PERCENTAGE]`: 95, 85, 100, etc.
- `[FILL_COLOR]`: Green (#4caf50), Cyan (#00ffff), Acid-green (#39ff14)
- `[DIMENSIONS]`: 1200x1200 or 1200x1600

---

## Quick Reference

### Style Selection
- Single impressive number? → **Metric Hero**
- Before/after comparison? → **Comparison Card**
- Progress or % completion? → **Progress Indicator**

### Color Coding
- **Success/Improvement**: Green (#4caf50), Acid-green (#39ff14)
- **Neutral/Data**: Cyan (#00ffff), Purple (#9933ff)
- **Warning/Problem**: Orange (#ff6600), Red (#ff0000)

---

## Version History

- **v1.0** (2025-12-24): Initial datacard styles optimized for bold metrics
