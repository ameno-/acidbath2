---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Frontend Design Skill

Create distinctive, production-grade frontend interfaces that avoid generic aesthetics.

## Design Thinking Process

Before coding, establish:
- **Purpose**: Problem-solving intent and target audience
- **Tone**: Distinct aesthetic direction (brutalist, luxury, playful, retro-futuristic, etc.)
- **Constraints**: Technical framework and performance requirements
- **Differentiation**: One memorable, unforgettable element

Execute with intentionality rather than intensity—refined minimalism and bold maximalism both succeed when purposeful.

## Production Requirements

- Production-grade quality and full functionality
- Visually striking, memorable design
- Cohesive aesthetic with clear point-of-view
- Meticulous refinement in every detail

## Aesthetic Focus Areas

- **Typography**: Distinctive font choices; avoid generic families
- **Color & Theme**: Cohesive palettes with dominant colors and sharp accents
- **Motion**: Page-load animations, scroll effects, hover micro-interactions
- **Spatial Composition**: Asymmetrical layouts, unexpected grids
- **Visual Details**: Gradients, textures, patterns, contextual effects

## Critical Constraints

Reject generic AI aesthetics: overused fonts, clichéd color schemes, predictable layouts. Vary approaches across projects; never converge on common defaults.

## ACIDBATH Brand Guidelines

- **Primary Accent**: #39ff14 (acid green)
- **Background**: #0a0a0a (near-black)
- **Alt Background**: #1a1a1a
- **Typography**: JetBrains Mono (mono), Inter (sans)
- **Tone**: Terminal-inspired, technical, hacker aesthetic
- **Font Weight**: Bold (800) for headings, uppercase transforms

## shadcn/ui Integration

This project uses shadcn/ui components. When creating UI:

1. **Use existing components**: Card, Badge, Button, Alert, Collapsible, ScrollArea
2. **Extend with variants**: Add custom variants that match acid-green theme
3. **Compose components**: Build complex UI from primitive shadcn components
4. **Maintain consistency**: Use CSS variables for colors (--primary, --accent, etc.)

## Component Location

- shadcn primitives: `src/components/ui/`
- Custom components: `src/components/`
- Astro layouts: `src/layouts/`
