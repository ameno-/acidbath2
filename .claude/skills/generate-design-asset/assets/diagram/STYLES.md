# Diagram Style Library

Style templates for diagram assets—simple 2-3 element technical representations. Diagrams are constrained by Nano Banana's limitations: **MAXIMUM 3 ELEMENTS**, **1-3 WORDS TOTAL**, abstract over accurate.

Dimensions: 1920x1080 or 2560x1440 pixels (16:9 landscape).

---

## CRITICAL: Diagram Nano Banana Limitations

⚠️ **STRICTEST CONSTRAINTS OF ALL ASSET TYPES**

1. **MAXIMUM 2-3 ELEMENTS** - Never attempt 4+ element diagrams (will fail)
2. **TEXT LIMIT: 1-3 words TOTAL** - One simple word per element maximum
3. **SIMPLE GEOMETRIC SHAPES ONLY** - Cubes, spheres, hexagons, cylinders
4. **ABSTRACT OVER ACCURATE** - Mood and concept, not technical precision
5. **GLOWING CONNECTIONS** - Energy streams, not arrows or complex connectors

**If concept requires >3 elements**: Use Abstract Representation (single element metaphor) instead.

---

## Style 1: Two-Element Flow

### Description
Two simple geometric elements connected by glowing line. Represents input→output, before→after, A→B relationships. Simplest diagram style.

### Nano Banana Prompt Template

```
Simple diagram showing two geometric elements connected by glowing line. Dark background, clean composition.

Elements:
- Left element: [SHAPE_1] in [COLOR_1] (e.g., "glowing cyan cube")
- Right element: [SHAPE_2] in [COLOR_2] (e.g., "glowing magenta sphere")
- Connection: [CONNECTION_TYPE] flowing from left to right (e.g., "cyan energy stream", "glowing particle flow")

Optional labels: [LABEL_1] on left element, [LABEL_2] on right element (1 word each, ALL CAPS).

Background: Deep black or charcoal. Clean, minimal.

Lighting: Element edges glow with their respective colors. Connection glows brightly.

Aesthetic: Clean, technical, simple relationship visualization.

Technical specifications: [DIMENSIONS] (1920x1080 or 2560x1440), 16:9 aspect ratio.
```

### Placeholder Variables
- `[SHAPE_1/2]`: Cube, sphere, hexagon, cylinder
- `[COLOR_1/2]`: Cyan, magenta, green, purple
- `[CONNECTION_TYPE]`: Energy stream, particle flow, glowing line
- `[LABEL_1/2]`: Optional 1-word labels ("INPUT", "OUTPUT", "DATA", "RESULT")
- `[DIMENSIONS]`: 1920x1080 or 2560x1440

---

## Style 2: Three-Element Process

### Description
Three elements in linear arrangement showing A→B→C flow. Maximum complexity for Nano Banana diagrams. Use for 3-stage processes only.

### Nano Banana Prompt Template

```
Isometric or linear diagram showing three geometric elements connected in sequence. Dark background.

Elements arranged left-to-right:
- Element 1: [SHAPE_1] in [COLOR_1]
- Element 2: [SHAPE_2] in [COLOR_2]
- Element 3: [SHAPE_3] in [COLOR_3]

Connections: Glowing [CONNECTION_COLOR] lines/streams connecting 1→2→3 in sequence.

Optional labels: [LABEL_1], [LABEL_2], [LABEL_3] (one word each, 3 words total maximum).

Background: Dark charcoal or black with subtle grid.

Aesthetic: Clean process flow, systematic progression.

Technical specifications: [DIMENSIONS], 16:9 aspect ratio.
```

### Placeholder Variables
- `[SHAPE_1/2/3]`: Simple geometric shapes
- `[COLOR_1/2/3]`: Distinct neon colors
- `[CONNECTION_COLOR]`: Cyan or white
- `[LABEL_1/2/3]`: "INPUT", "PROCESS", "OUTPUT" or similar
- `[DIMENSIONS]`: 1920x1080 or 2560x1440

---

## Style 3: Abstract Representation

### Description
Single element with atmospheric effects suggesting concept metaphorically. Use when literal diagram would be too complex or when concept is abstract.

### Nano Banana Prompt Template

```
Single [OBJECT_TYPE] floating in dark space representing [CONCEPT] through visual metaphor.

The object: [DETAILED_DESCRIPTION] with [MATERIAL_TYPE] rendering. Atmospheric effects suggest concept without literal depiction.

Background: Deep black with [ATMOSPHERE_TYPE] (particle systems, depth fog, subtle glow).

Lighting: [LIGHTING_DESCRIPTION] creating mood.

NO text. Pure visual metaphor.

Technical specifications: [DIMENSIONS], 16:9 aspect ratio.
```

### Placeholder Variables
- `[OBJECT_TYPE]`: Sphere, cube, abstract form
- `[CONCEPT]`: What it represents
- `[DETAILED_DESCRIPTION]`: Object details
- `[MATERIAL_TYPE]`: Glass, holographic, glowing
- `[ATMOSPHERE_TYPE]`: Particle effects, fog, glow
- `[LIGHTING_DESCRIPTION]`: Lighting mood
- `[DIMENSIONS]`: 1920x1080 or 2560x1440

---

## CRITICAL WARNINGS

### Do NOT Attempt
❌ 4+ element diagrams (use Abstract Representation instead)
❌ Complex flowcharts with multiple paths
❌ Detailed system architectures
❌ Diagrams with 4+ words of text

### Always Remember
✅ Maximum 3 elements
✅ Simple geometric shapes only
✅ Abstract over literal
✅ 0-3 words total text

---

## Version History

- **v1.0** (2025-12-24): Initial diagram styles with strict Nano Banana limitations
