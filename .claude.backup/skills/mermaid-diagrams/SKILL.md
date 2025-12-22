---
name: mermaid-diagrams
description: Create Mermaid diagrams from prompts, descriptions, or existing content (ASCII art, text). Use when creating flowcharts, sequence diagrams, architecture diagrams, or converting ASCII art to proper diagrams.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Mermaid Diagram Generation

Create professional diagrams using Mermaid syntax. This skill handles:
- Creating diagrams from text descriptions or requirements
- Converting ASCII art to Mermaid
- All Mermaid diagram types
- **Verification that diagrams render correctly**

## CRITICAL: Verification Step

**ALWAYS verify diagrams render before completing the task.**

After creating or modifying any Mermaid diagram, run this verification:

```bash
# Create temp file with the diagram
cat << 'MERMAID_EOF' > /tmp/mermaid-test.mmd
<paste diagram content here>
MERMAID_EOF

# Verify it parses correctly (will output errors if invalid)
npx -y @mermaid-js/mermaid-cli mmdc -i /tmp/mermaid-test.mmd -o /tmp/mermaid-test.svg 2>&1
```

**If verification fails:**
1. Read the error message carefully
2. Fix the syntax issue (common problems listed below)
3. Re-verify until it passes
4. Only then consider the diagram complete

### Common Verification Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Parse error` | Invalid syntax | Check brackets, arrows, quotes |
| `Unexpected token` | Special chars in labels | Wrap label in quotes: `["Label"]` |
| `Unknown diagram type` | Typo in diagram type | Use exact: `flowchart`, `sequenceDiagram`, etc. |
| `Unterminated string` | Missing closing quote | Ensure all `"` are paired |
| `Invalid direction` | Wrong flowchart direction | Use: `TD`, `TB`, `BT`, `LR`, `RL` |

## Diagram Types Reference

### Flowchart (most common)
```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

**Node shapes:**
- `[text]` - Rectangle
- `(text)` - Rounded rectangle
- `{text}` - Diamond (decision)
- `((text))` - Circle
- `[[text]]` - Subroutine
- `[(text)]` - Cylinder (database)
- `{{text}}` - Hexagon

**Directions:** `TD` (top-down), `TB`, `BT`, `LR` (left-right), `RL`

### Sequence Diagram
```mermaid
sequenceDiagram
    participant U as User
    participant S as Server
    participant D as Database

    U->>S: Request
    S->>D: Query
    D-->>S: Results
    S-->>U: Response

    Note over S,D: Processing happens here
```

**Arrow types:**
- `->` solid line
- `-->` dotted line
- `->>` solid with arrowhead
- `-->>` dotted with arrowhead
- `-x` solid with X
- `--x` dotted with X

### Block Diagram (for boxes/containers)
```mermaid
block-beta
    columns 3

    block:group1
        A["Item A"]
        B["Item B"]
    end

    C["Standalone"]

    block:group2
        D["Item D"]
        E["Item E"]
    end
```

### Architecture Diagram
```mermaid
architecture-beta
    group api(cloud)[API Layer]

    service server(server)[Server] in api
    service db(database)[Database] in api

    server:R -- L:db
```

### Class Diagram
```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +fetch()
    }
    Animal <|-- Dog
```

### State Diagram
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: start
    Processing --> Complete: finish
    Processing --> Error: fail
    Complete --> [*]
    Error --> Idle: retry
```

### Entity Relationship
```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
    USER {
        int id PK
        string name
    }
```

### Gantt Chart
```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
        Task A: a1, 2024-01-01, 7d
        Task B: a2, after a1, 5d
```

### Pie Chart
```mermaid
pie title Distribution
    "Category A": 40
    "Category B": 30
    "Category C": 30
```

## Converting ASCII Art

When converting ASCII box diagrams:

1. **Identify the structure type:**
   - Boxes with arrows → `flowchart`
   - Sequential steps with participants → `sequenceDiagram`
   - Nested boxes/containers → `block-beta`
   - Tables with relationships → `erDiagram`

2. **Extract content:**
   - Box titles become node labels
   - Arrows become connections
   - Text inside boxes becomes node content

3. **Map ASCII elements:**
   | ASCII | Mermaid |
   |-------|---------|
   | `┌───┐` box | `[label]` node |
   | `→` or `──▶` | `-->` arrow |
   | `│` vertical | subgraph or sequence |
   | Nested boxes | `subgraph` or `block` |

## Best Practices

1. **Keep it simple** - Mermaid renders better with fewer elements
2. **Use subgraphs** for grouping related items
3. **Label edges** when the relationship isn't obvious
4. **Use consistent direction** - usually TD or LR
5. **Escape special characters** in labels with quotes: `["Label with (parens)"]`

## Styling

```mermaid
flowchart LR
    A[Node A]:::highlight --> B[Node B]

    classDef highlight fill:#ffccbc,stroke:#ff5722
    classDef default fill:#e3f2fd,stroke:#2196f3
```

## Common Patterns

### Parent-Child Delegation
```mermaid
sequenceDiagram
    participant P as Parent
    participant F as FileSystem
    participant S as Sub-Agent

    P->>F: Write context.md
    P->>S: Research task
    S->>F: Read context.md
    S->>S: Do work
    S->>F: Write report.md
    S-->>P: Done
    P->>F: Read report.md
```

### Architecture Layers
```mermaid
flowchart TB
    subgraph UI[UI Layer]
        A[Component]
    end
    subgraph BL[Business Logic]
        B[Service]
    end
    subgraph DA[Data Access]
        C[Repository]
    end

    A --> B --> C
```

### Decision Flow
```mermaid
flowchart TD
    Start([Start]) --> Check{Condition?}
    Check -->|Yes| Action1[Do This]
    Check -->|No| Action2[Do That]
    Action1 --> End([End])
    Action2 --> End
```

## Complete Workflow

**Follow this workflow for every diagram task:**

1. **Understand the requirement**
   - Read any source content (ASCII art, description, existing diagram)
   - Identify the appropriate diagram type

2. **Create the diagram**
   - Write the Mermaid syntax
   - Follow best practices (simple, labeled, consistent direction)

3. **Verify the diagram renders** (REQUIRED)
   ```bash
   cat << 'MERMAID_EOF' > /tmp/mermaid-test.mmd
   flowchart TD
       A[Your] --> B[Diagram]
   MERMAID_EOF
   npx -y @mermaid-js/mermaid-cli mmdc -i /tmp/mermaid-test.mmd -o /tmp/mermaid-test.svg 2>&1
   ```

4. **Fix any errors**
   - If verification fails, fix the syntax
   - Re-run verification until it passes

5. **Write the diagram to file**
   - Only after verification passes
   - Use `.mmd` extension for standalone files
   - Or embed in markdown with ` ```mermaid ` fence

6. **Confirm completion**
   - Report the verification result to the user
   - Include the file path where the diagram was saved
