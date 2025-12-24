---
title: "Directory Watchers: File-Based AI Automation That Scales"
description: "Turn your file system into an AI interface. Build drop zones that process files automatically with working Python code and production considerations."
pubDate: 2025-12-15
author: "Acidbath"
tags: ["ai", "automation", "file-system", "python", "production"]
banner: "/assets/posts/directory-watchers-banner.png"
category: "Production Patterns"
difficulty: "Intermediate"
tldr: "Directory watchers turn your file system into an AI interface—drop a file, get processed results. Build with Python's watchdog library, configure zones via YAML, and handle production concerns like race conditions, error recovery, and monitoring."
keyTakeaways:
  - "Drop zones eliminate the chat interface—drag a file, get results automatically"
  - "Use watchdog events with pattern matching for flexible zone configuration"
  - "Production concerns: file locks, race conditions, atomic moves, error recovery"
  - "Archive originals before processing for debugging and audit trails"
  - "Add monitoring with simple JSON logs and file-based alerts for reliability"
---

Directory watchers turn your file system into an AI interface.

Drag a file into a folder. An agent processes it automatically. You get results. No chat. No prompting. No human-in-the-loop.

This post shows you how to build a complete drop zone system with working Python code, then walks through what breaks in production and how to fix it.

## The Architecture

```mermaid
flowchart TB
    subgraph DROPS["~/drops/"]
        D1["transcribe/"] --> W1["Whisper → text"]
        D2["analyze/"] --> W2["Claude → summary"]
        D3["images/"] --> W3["Replicate → generations"]
        D4["data/"] --> W4["Claude → analysis"]
    end

    subgraph WATCHER["DIRECTORY WATCHER"]
        E1[watchdog events] --> E2[Pattern Match] --> E3[Agent Execute]
    end

    DROPS --> WATCHER

    subgraph OUTPUT["OUTPUTS"]
        O1["~/output/{zone}/{timestamp}-{filename}.{result}"]
        O2["~/archive/{zone}/{timestamp}-{filename}.{original}"]
    end

    WATCHER --> OUTPUT

    style DROPS fill:#e3f2fd
    style WATCHER fill:#fff3e0
    style OUTPUT fill:#c8e6c9
```

## POC: Complete Drop Zone System

### Step 1: Configuration File

Create `drops.yaml`:

```yaml
# Drop Zone Configuration
# Each zone watches a directory and triggers an agent on file events

output_dir: ~/output
archive_dir: ~/archive
log_dir: ~/logs

zones:
  transcribe:
    directory: ~/drops/transcribe
    patterns: ["*.mp3", "*.wav", "*.m4a", "*.webm"]
    agent: whisper_transcribe
    events: [created]

  analyze:
```

> ** Complete Example:** [Step Configuration File](https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/step-configuration-file)
>
> Complete implementation from the 'Step 1: Configuration File' section.
>
> **Language:** yaml | **Lines:** 51

### Step 2: The Core Watcher

Create `drop_watcher.py`:

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "watchdog>=4.0.0",
#   "pyyaml>=6.0",
#   "rich>=13.0.0",
#   "anthropic>=0.40.0",
# ]
# ///
"""
Drop Zone Watcher - File-based AI automation

Usage:
    uv run drop_watcher.py [--config drops.yaml]

```

> ** Complete Example:** [Step Core Watcher](https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/step-core-watcher)
>
> Complete implementation from the 'Step 2: The Core Watcher' section.
>
> **Language:** python | **Lines:** 218

### Step 3: Agent Prompt Templates

Create `prompts/analyze.md`:

```markdown
# Document Analysis Agent

Analyze the following document and provide a structured summary.

## Document Content

{content}

## Output Format

Provide your analysis in this format:

### Summary
A 2-3 sentence overview of the document.

### Key Points
- Bullet point list of main ideas

### Topics Covered
- List of topics/themes

### Action Items (if applicable)
- Numbered list of action items

### Questions Raised
- Questions that arise from this content

### Confidence
How confident are you in this analysis? (high/medium/low) and why.
```

Create `prompts/data_analysis.md`:

```markdown
# Data Analysis Agent

Analyze the following data file and provide insights.

## Data Content

{content}

## Filename
{filename}

## Analysis Required

1. **Data Overview**
   - File format (CSV, JSON, etc.)
   - Number of records/rows
   - Column/field names

2. **Statistical Summary**
   - For numeric columns: min, max, mean, median
   - For categorical columns: unique values, distribution

3. **Data Quality**
   - Missing values
   - Potential outliers
   - Data type issues

4. **Insights**
   - Key patterns or trends
   - Notable correlations
   - Anomalies worth investigating

5. **Recommendations**
   - Suggested next steps for analysis
   - Visualization recommendations
   - Data cleaning suggestions
```

### Step 4: Image Generation Agent

Create `agents/image_gen.py`:

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "replicate>=0.25.0",
#   "requests>=2.31.0",
# ]
# ///
"""
Image Generation Agent

Reads prompts from a text file and generates images using Replicate.
Each line in the file is a separate prompt.
"""

import os
import sys
from datetime import datetime
# ... continues with image generation logic
```

> ** Complete Example:** [Image Generation Agent](https://github.com/ameno-/acidbath-code/tree/main/production-patterns/directory-watchers/step-image-generation)
>
> Complete image generation agent using Replicate API. Processes text files containing prompts and downloads generated images.
>
> **Language:** python | **Lines:** 76

## Data Flow: File Drop to Result

```mermaid
flowchart LR
    subgraph Input
        A[User drops file.txt]
    end

    subgraph Watcher
        B[Watchdog detects create event]
        C[Pattern matches *.txt]
        D[Agent selected: claude_analyze]
    end

    subgraph Agent
        E[Load prompt template]
        F[Read file content]
        G[Call Claude API]
        H[Write result.md]
    end

    subgraph Cleanup
        I[Archive original]
        J[Log completion]
    end

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J

    style A fill:#e8f5e9
    style H fill:#e3f2fd
    style J fill:#fff3e0
```

## When Drop Zones Fail

The POC above works for clean, isolated files. Production breaks in predictable ways.

### Files That Need Context

A code file dropped into a review zone lacks its dependencies, imports, and surrounding architecture. The agent sees `import UserService from '../services'` but doesn't know what UserService does.

**What breaks:** Reviews are shallow. "This looks fine" instead of "This violates the retry policy established in commit abc123."

**Fix:** Add a context builder. Before processing, scan the repository for related files:

```python
def gather_context(filepath: str) -> dict:
    """Gather related files for context."""
    context = {"main_file": filepath}

    # Parse imports
    with open(filepath) as f:
        content = f.read()
        imports = extract_imports(content)  # Your parser here

    # Find imported files
    related = []
    for imp in imports:
        path = resolve_import(imp, filepath)
        if path and os.path.exists(path):
            with open(path) as f:
                related.append({"path": path, "content": f.read()})

    context["related_files"] = related
    return context
```

This increases token usage 3-5x but improves accuracy significantly. For a 200-line Python file with 8 imports, you go from 800 tokens to 3,200 tokens. Cost per review goes from $0.02 to $0.08 with claude-3-5-sonnet-20241022.

### Multi-File Inputs

Sometimes the task requires multiple files processed together. A blog post draft plus supporting research notes. Three screenshots that show a UI flow. CSV data plus its schema definition.

**What breaks:** The watcher processes files individually. Drop three related screenshots, get three unconnected analyses instead of one coherent flow analysis.

**Fix:** Add a staging area with batch processing:

```yaml
# In drops.yaml
ui_review:
  directory: ~/drops/ui-review
  patterns: ["*.png", "*.jpg"]
  agent: ui_flow_analyzer
  batch_mode: true
  batch_window: 30  # seconds
  batch_trigger: 3  # or N files
```

Buffer files for 30 seconds. If 3+ files arrive, process as a batch. If timeout hits with fewer files, process what you have.

### Race Conditions: Incomplete Writes

You drop a 500MB video file. Watchdog fires on create. The agent starts processing while the file is still copying. Whisper transcribes 8 seconds of a 45-minute video.

**What breaks:** Partial processing. Silent failures. Confusing output.

**Fix:** Verify file stability before processing:

```python
def wait_for_stable_file(filepath: str, timeout: int = 30) -> bool:
    """Wait until file size stops changing."""
    last_size = -1
    stable_count = 0

    for _ in range(timeout):
        try:
            current_size = os.path.getsize(filepath)
            if current_size == last_size:
                stable_count += 1
                if stable_count >= 3:  # Stable for 3 seconds
                    return True
            else:
                stable_count = 0
            last_size = current_size
        except OSError:
            pass
        time.sleep(1)

    return False
```

Replace the POC's `time.sleep(0.5)` with this. A 500MB file takes 6-10 seconds to copy on typical hardware. Three-second stability window catches 99% of cases without excessive waiting.

### Agent Failures Mid-Processing

API rate limit hit. Network timeout. Model refuses the prompt due to content policy. The agent fails after archiving the input file but before writing output.

**What breaks:** Input file is gone. No output exists. No way to retry. User thinks it worked because no error appeared.

**Fix:** Transactional processing with rollback:

```python
def _process_file(self, filepath: str):
    if not self._matches_pattern(filepath):
        return

    # Create processing record
    processing_id = self._start_processing(filepath)

    try:
        output_path = self._run_agent(filepath)
        self._archive_file(filepath)
        self._mark_complete(processing_id, output_path)
        console.print(f"[green]✓[/] Output: {output_path}")
    except Exception as e:
        self._mark_failed(processing_id, str(e))
        # Don't archive on failure - leave for retry
        console.print(f"[red]✗[/] Error: {e}")
        # Write error details to dead letter queue
        self._write_to_dlq(filepath, processing_id, e)
```

Keep failed files in place. Log failures to a dead letter queue. Provide a manual retry command. For our use case running 200 files/day, we see 3-5 transient failures per day. All are recoverable with retry.

### Token Limit Exceeded

A 15,000-line CSV file hits the analyze zone. The agent tries to stuff it all into a prompt. Claude returns a 400 error: maximum context length exceeded.

**What breaks:** Processing fails. File size limits aren't obvious. No graceful degradation.

**Fix:** Add size checks and chunking strategy:

```python
def _check_size_limits(self, filepath: str) -> tuple[bool, str]:
    """Check if file is processable."""
    file_size = os.path.getsize(filepath)
    max_size = self.agent_config.get("max_file_size", 10 * 1024 * 1024)  # 10MB default

    if file_size > max_size:
        return False, f"File too large: {file_size} bytes (max: {max_size})"

    # For text files, estimate tokens
    if filepath.endswith(('.txt', '.md', '.csv', '.json')):
        with open(filepath) as f:
            content = f.read()
        estimated_tokens = len(content) // 4  # Rough estimate
        max_tokens = self.agent_config.get("max_tokens", 100000)

        if estimated_tokens > max_tokens:
            return False, f"Content too large: ~{estimated_tokens} tokens (max: {max_tokens})"

    return True, "OK"
```

For a 200K-token model, set max_tokens to 150K to leave room for prompts and output. Files that exceed limits go to a manual review folder with a clear error message.

### Files Requiring Human Review

Some automation needs a human checkpoint. Legal contract analysis that might inform business decisions. Code deployments to production. Financial data processing.

**What breaks:** Full automation isn't always desirable. No way to inject human judgment. Liability concerns.

**Fix:** Add an approval workflow:

```yaml
contracts:
  directory: ~/drops/contracts
  patterns: ["*.pdf"]
  agent: contract_analyzer
  approval_required: true
  approval_timeout: 3600  # 1 hour
```

```python
def _process_file(self, filepath: str):
    output_path = self._run_agent(filepath)

    if self.zone_config.get("approval_required"):
        approval_path = self._move_to_approval_queue(filepath, output_path)
        console.print(f"[yellow]⏸[/] Awaiting approval: {approval_path}")
        self._notify_approver(approval_path)
        # Don't archive yet - wait for approval
    else:
        self._archive_file(filepath)
```

Set up an approval directory. Agent processes the file and moves it there with its output. Human reviews both. Approve by dropping in `~/approvals/accept/`, reject to `~/approvals/reject/`. A second watcher handles the approval directories.

## Production Deployment Considerations

POC works on your laptop. Production needs operational rigor.

### Monitoring and Alerting

**The problem:** Silent failures. You think it's working. It's been down for three days.

**What to track:**

1. **Processing rate:** Files processed per hour
2. **Failure rate:** Percentage of files that fail
3. **Processing latency:** Time from drop to output
4. **Queue depth:** Files waiting in drop zones
5. **API health:** Response times and error rates

Instrument the watcher:

```python
import statsd  # Or your metrics library

metrics = statsd.StatsClient('localhost', 8125)

def _process_file(self, filepath: str):
    start_time = time.time()

    try:
        output_path = self._run_agent(filepath)
        self._archive_file(filepath)

        # Record success
        metrics.incr(f'dropzone.{self.zone_name}.success')
        metrics.timing(f'dropzone.{self.zone_name}.duration',
                      (time.time() - start_time) * 1000)
    except Exception as e:
        metrics.incr(f'dropzone.{self.zone_name}.failure')
        raise
```

Set alerts:
- Processing rate drops below 10 files/hour when average is 50/hour
- Failure rate exceeds 10% over a 15-minute window
- No files processed in 2 hours during business hours
- Queue depth exceeds 100 files

For our production deployment handling 800 files/day, we get 1-2 actionable alerts per week. Most are transient API issues that self-resolve.

### Logging and Audit Trails

Every file processed needs a record: who dropped it, when, what agent processed it, what the output was, any errors encountered.

```python
import json
import logging

logging.basicConfig(
    filename=os.path.expanduser("~/logs/dropzone.log"),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def _process_file(self, filepath: str):
    processing_record = {
        "timestamp": datetime.now().isoformat(),
        "zone": self.zone_name,
        "agent": self.agent_name,
        "input_file": filepath,
        "file_size": os.path.getsize(filepath),
        "user": os.environ.get("USER"),
    }

    try:
        output_path = self._run_agent(filepath)
        processing_record["status"] = "success"
        processing_record["output_file"] = output_path
        processing_record["output_size"] = os.path.getsize(output_path)
    except Exception as e:
        processing_record["status"] = "failure"
        processing_record["error"] = str(e)
        processing_record["error_type"] = type(e).__name__
    finally:
        processing_record["duration_seconds"] = time.time() - start_time
        logging.info(json.dumps(processing_record))
```

Logs go to structured JSON for easy parsing. Ship to your log aggregation service. When a user asks "did my file process?", you have answers.

### Resource Limits

**CPU and Memory:** Watchdog is lightweight, but agents aren't. Whisper transcription spikes CPU to 100% for 30-60 seconds per file. Claude Code execution can use 2GB RAM.

Set process limits:

```python
import resource

def _run_agent(self, filepath: str) -> str:
    # Limit memory to 4GB
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))

    # Limit CPU time to 5 minutes
    resource.setrlimit(resource.RLIMIT_CPU, (300, 300))

    # Run agent...
```

**API Rate Limits:** Claude API: 50 requests/minute on tier 1, 5,000 requests/minute on tier 4. Replicate varies by model.

Add rate limiting:

```python
from time import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = deque()

    def acquire(self):
        now = time()
        # Remove old requests outside window
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()

        if len(self.requests) >= self.max_requests:
            sleep_time = self.requests[0] + self.window - now
            time.sleep(sleep_time)

        self.requests.append(now)

# In agent code
rate_limiter = RateLimiter(max_requests=45, window_seconds=60)

def _run_claude_agent(self, filepath: str, output_dir: str) -> str:
    rate_limiter.acquire()
    # Call API...
```

Leave headroom. 45 requests/minute for a 50 req/min limit. Shared rate limiters if you have multiple services using the same API key.

### Graceful Degradation

APIs go down. Networks fail. Disk fills up. Production systems need fallbacks.

**When Claude API is unavailable:**

```python
def _run_claude_agent(self, filepath: str, output_dir: str) -> str:
    try:
        # Normal Claude processing
        return self._call_claude_api(filepath, output_dir)
    except anthropic.APIConnectionError:
        # Fallback to queue
        return self._queue_for_retry(filepath)
    except anthropic.RateLimitError:
        # Back off and retry once
        time.sleep(60)
        return self._call_claude_api(filepath, output_dir)
```

**When disk space is low:**

```python
def _check_disk_space(self) -> bool:
    stat = os.statvfs(os.path.expanduser("~/output"))
    free_bytes = stat.f_bavail * stat.f_frsize
    free_gb = free_bytes / (1024**3)

    if free_gb < 1.0:  # Less than 1GB free
        console.print("[red]Low disk space![/] Pausing processing.")
        return False
    return True
```

Check before each file. Pause processing if disk is full. Alert on low space. For systems processing 50GB/day, check every 10 files and alert at 10GB free.

### Security: Validating File Contents

Users drop files. Users are unpredictable. Protect your system.

**File type validation:**

```python
import magic  # python-magic library

def _validate_file(self, filepath: str) -> tuple[bool, str]:
    # Check declared extension matches actual content
    mime = magic.from_file(filepath, mime=True)

    allowed_types = self.zone_config.get("allowed_mime_types", [])
    if allowed_types and mime not in allowed_types:
        return False, f"Invalid file type: {mime}"

    # Check for malicious content
    if mime.startswith("application/x-executable"):
        return False, "Executable files not allowed"

    return True, "OK"
```

**Content sanitization:**

```python
def _sanitize_content(self, content: str) -> str:
    # Remove potential injection attacks
    content = content.replace("```python", "```text")
    content = content.replace("```bash", "```text")

    # Limit size
    max_chars = 500000  # ~125K tokens
    if len(content) > max_chars:
        content = content[:max_chars] + "\n\n[Content truncated]"

    return content
```

Never execute code from dropped files directly. Treat all input as untrusted. Validate, sanitize, then process.

## The Automation Decision Framework

Not every task deserves automation. Use specific thresholds.

| Frequency | ROI Threshold | Action |
|-----------|---------------|--------|
| Once | N/A | Use chat |
| 2-5x/month | > 5 min saved | Maybe automate |
| Weekly | > 2 min saved | Consider zone |
| Daily | > 30 sec saved | Build zone |
| 10+ times/day | Any time saved | Definitely zone |

## Real-World Examples

### Voice Memo Processing

```yaml
# In drops.yaml
morning_debrief:
  directory: ~/drops/debrief
  patterns: ["*.m4a", "*.mp3", "*.wav"]
  agent: debrief_processor
  events: [created]

agents:
  debrief_processor:
    type: bash
    command: |
      # Transcribe
      whisper "{file}" -o /tmp --output_format txt

      # Extract filename for transcript
      BASENAME=$(basename "{file}" | sed 's/\.[^.]*$//')

      # Process with Claude
      cat /tmp/$BASENAME.txt | claude --prompt "$(cat prompts/debrief.md)" > "{output_dir}/$BASENAME-insights.md"
```

### Code Review Zone

```yaml
code_review:
  directory: ~/drops/review
  patterns: ["*.py", "*.ts", "*.js", "*.go"]
  agent: code_review
  events: [created]

agents:
  code_review:
    type: claude
    prompt_file: prompts/code_review.md
    model: claude-sonnet-4-20250514
```

### Research Paper Zone

```yaml
research:
  directory: ~/drops/papers
  patterns: ["*.pdf"]
  agent: paper_summarize
  events: [created]

agents:
  paper_summarize:
    type: python
    script: agents/paper_processor.py
```

## Running the System

```bash
# Create the directory structure
mkdir -p ~/drops/{transcribe,analyze,images,data}
mkdir -p ~/output ~/archive ~/logs
mkdir -p prompts agents

# Start the watcher
uv run drop_watcher.py --config drops.yaml

# In another terminal, test it:
echo "Write a blog post about AI automation" > ~/drops/analyze/test.txt

# Check output
ls ~/output/analyze/
cat ~/output/analyze/*.md
```

## The Key Insight

**Repeat workflows benefit most from automation.**

The first time you do something, chat is fine. The tenth time, you should have a drop zone.

Directory watchers work because they match how you already work. You already organize files into folders. You already drag and drop. The interface is invisible.

They're called agents for a reason. They're capable of agency. Lean into the autonomy.

---

**Key Takeaways:**
- Directory watchers turn the file system into an AI interface with zero learning curve
- YAML config makes adding new zones a 5-minute task
- Pattern matching routes files to appropriate agents automatically
- Production requires monitoring, logging, rate limiting, and error handling
- Failure modes are predictable: context gaps, race conditions, size limits, approval needs
- ROI threshold: anything you do 10+ times/week that takes more than 30 seconds
- Start with your highest-frequency task and expand from there

**Try It Now:**
Copy `drop_watcher.py` and `drops.yaml` above. Create the directory structure. Start the watcher. Drop a text file into `~/drops/analyze/`. Watch it process automatically and check `~/output/analyze/` for results.
