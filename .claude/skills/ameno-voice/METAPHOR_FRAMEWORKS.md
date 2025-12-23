# Metaphor Frameworks

Technical concepts map better to construction and engineering metaphors. This library provides ready-to-use frameworks for explaining complex ideas.

---

## 1. Building a Bridge

**Best for**: APIs, integrations, connecting systems, load handling

### Concept Mapping

| Technical Concept | Bridge Equivalent |
|-------------------|-------------------|
| API endpoint | Bridge entrance/exit |
| Request payload | Traffic crossing |
| Rate limiting | Load capacity |
| Authentication | Toll booth / checkpoint |
| Error handling | Structural supports |
| Timeout | Bridge closure time |
| Retry logic | Detour routes |
| Load balancing | Multiple lanes |

### Sample Explanations

**APIs**: "An API is a bridge between two systems. You don't need to know how the other city works - you just need to know the bridge exists and what format your cargo needs to be in to cross."

**Rate Limiting**: "Every bridge has a weight limit. Send too many trucks at once and the structure fails. Rate limiting is posting the 'Max 5 trucks per minute' sign before disaster hits."

**Authentication**: "The toll booth at the bridge entrance. You need a valid ticket (token) to cross. No ticket? You're not getting to the other side."

---

## 2. Train System

**Best for**: Pipelines, sequential processing, data flow, routing

### Concept Mapping

| Technical Concept | Train Equivalent |
|-------------------|------------------|
| Pipeline | Train tracks |
| Data packet | Cargo car |
| Endpoint | Station |
| Routing | Track switches |
| Queue | Train waiting at platform |
| Middleware | Inspection points |
| Backpressure | Traffic congestion |
| Batch processing | Full train departure |

### Sample Explanations

**Pipelines**: "Data flows through your system like a train on tracks. Each station (function) processes the cargo and passes it to the next stop. The train doesn't skip stations."

**Routing**: "When data hits a junction, the switch decides which track to take. `if` statements are your track switches - they route the train based on the cargo manifest."

**Queues**: "The train sits at the platform until it's full or the scheduled departure time hits. That's batching - don't send half-empty trains when you can wait for efficiency."

---

## 3. Building a House

**Best for**: Architecture, dependencies, layered systems, foundations

### Concept Mapping

| Technical Concept | House Equivalent |
|-------------------|------------------|
| Foundation | Database / core models |
| Framing | Application structure |
| Plumbing | Data flow infrastructure |
| Electrical | Event systems / signals |
| Finishing | UI / presentation layer |
| Dependencies | Building materials |
| Refactoring | Renovation |
| Technical debt | Shortcuts during construction |

### Sample Explanations

**Architecture Layers**: "You can't hang drywall without studs. You can't install studs without a foundation. Your app has the same layers - database before logic, logic before UI."

**Technical Debt**: "Every shortcut during construction comes due eventually. That 'temporary' wire you ran through the wall? You'll be tearing out drywall to fix it later."

**Dependencies**: "You don't manufacture your own nails. You buy them. Dependencies are your building materials - someone else made them, you just use them right."

---

## 4. Factory Assembly Line

**Best for**: Automation, workflows, throughput, quality control

### Concept Mapping

| Technical Concept | Factory Equivalent |
|-------------------|-------------------|
| Workflow | Assembly line |
| Function | Work station |
| Input validation | Quality inspection |
| Error handling | Reject bin |
| Parallelism | Multiple lines |
| Bottleneck | Slowest station |
| Scaling | Adding shifts |
| Testing | QA checkpoint |

### Sample Explanations

**Workflows**: "Each station on the line does one thing. Station 1 attaches wheels. Station 2 installs seats. Your functions should work the same way - one job per station."

**Bottlenecks**: "Your factory outputs at the speed of your slowest station. If painting takes 10 minutes and everything else takes 1, you've got 9 minutes of waiting at every other station."

**Parallelism**: "Why run one assembly line when you can run four? As long as they don't need the same tools at the same time, more lines = more throughput."

---

## 5. Power Grid

**Best for**: Distribution, scaling, load balancing, redundancy

### Concept Mapping

| Technical Concept | Grid Equivalent |
|-------------------|-----------------|
| Server | Power plant |
| Load balancer | Transformer |
| CDN | Substation |
| Cache | Battery storage |
| Failover | Backup generator |
| Scaling | Adding capacity |
| Peak load | Summer AC demand |
| Circuit breaker | Fuse / breaker |

### Sample Explanations

**Load Balancing**: "A transformer doesn't power your house directly from the plant. It steps down the voltage and distributes the load. Your load balancer does the same - splits incoming traffic so no single server melts."

**Caching**: "Battery storage holds power for when demand spikes. Your cache holds data for when requests spike. Pre-store what you'll need instead of generating it fresh every time."

**Circuit Breakers**: "When the circuit overloads, the breaker trips. Better to cut one circuit than burn down the house. Circuit breaker patterns in code work the same - fail fast, fail safe."

---

## 6. Plumbing System

**Best for**: Streams, data flow, input/output, backpressure

### Concept Mapping

| Technical Concept | Plumbing Equivalent |
|-------------------|---------------------|
| Data stream | Water flow |
| Buffer | Tank / reservoir |
| Backpressure | Pipe pressure |
| Valve | Gate / filter |
| Drainage | Cleanup / disposal |
| Leak | Memory leak |
| Clog | Blocked queue |
| Main line | Primary data path |

### Sample Explanations

**Streams**: "Data flows through your system like water through pipes. You don't bucket it and carry it - you open the tap and let it flow to where it's needed."

**Backpressure**: "Turn on every faucet in your house and the pressure drops. Same thing happens when you push more data than your system can handle. Either the pressure drops (slowdown) or pipes burst (crash)."

**Memory Leaks**: "A dripping faucet wastes water slowly. A memory leak wastes RAM slowly. Both seem minor until you get the bill."

---

## Usage Guidelines

### Choosing the Right Framework

| If explaining... | Use this framework |
|------------------|-------------------|
| System connections | Bridge |
| Data pipelines | Train |
| Software architecture | House |
| Automation workflows | Factory |
| Scaling / distribution | Power Grid |
| Stream processing | Plumbing |

### Framework Rules

1. **Pick one framework per concept** - Don't mix metaphors
2. **Acknowledge limits** - "The analogy breaks down when..."
3. **Return to technical** - Always map back to the actual concept
4. **Keep it brief** - One paragraph max, then code
5. **Match reader's world** - Engineers know these systems
