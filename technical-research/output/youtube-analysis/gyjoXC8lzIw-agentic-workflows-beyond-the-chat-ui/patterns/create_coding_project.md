# PROJECT:
Build agentic drop zone system for automating file-based AI workflows through directory monitoring.

# SUMMARY:
The Agentic Drop Zone is a file-based workflow automation system that monitors directories for file drops and triggers specialized AI agents to process them. Users drag files into specific directories which automatically execute predefined prompts using various AI agents (Claude, Gemini, etc.). The system supports parallel processing, agent-agnostic workflows, and configurable drop zones defined in a YAML file. Examples include image generation, transcription, finance processing, and data augmentation - all triggered by simple file drops.

# STEPS:
1. Create YAML configuration file defining drop zones and their triggers
2. Set up directory watchers using Python's watchdog library for monitoring
3. Define prompt templates with variable substitution for file paths
4. Implement agent abstraction layer supporting multiple AI providers via SDKs
5. Build file pattern matching system for triggering appropriate workflows
6. Create parallel processing framework for handling multiple simultaneous drops
7. Add rich terminal logging for real-time workflow status updates
8. Implement automatic file archiving after successful processing completion
9. Design modular prompt system with reusable components and sections
10. Configure environment variables for different AI service API keys
11. Build error handling and retry mechanisms for failed workflows
12. Create output directory management for generated assets and results
13. Add workflow validation to ensure proper configuration before execution
14. Implement streaming response handling for real-time agent communication
15. Package entire system as single-file script using UV dependencies
16. Test workflows with sample files and validate output quality

# STRUCTURE:
```
agentic-drop-zone/
├── adz.py                    # Main single-file application
├── drops.yaml               # Drop zone configuration
├── prompts/                 # Prompt templates directory
│   ├── echo.md             # Simple echo workflow
│   ├── create_image.md     # Image generation workflow
│   ├── edit_image.md       # Image editing workflow
│   ├── morning_debrief.md  # Audio transcription workflow
│   ├── expand_training.md  # Data augmentation workflow
│   └── finance_categorize.md # Finance processing workflow
├── zones/                   # Drop zone directories
│   ├── echo/               # Echo test zone
│   ├── gemini_echo/        # Gemini-specific echo zone
│   ├── generate_images/    # Image generation zone
│   ├── edit_images/        # Image editing zone
│   ├── morning_debrief/    # Audio processing zone
│   ├── expand_training_data/ # Data expansion zone
│   └── finance/            # Finance categorization zone
├── output/                  # Generated output directory
│   ├── images/             # Generated images
│   ├── transcripts/        # Audio transcriptions
│   ├── finance/            # Finance reports
│   └── training_data/      # Expanded datasets
├── archive/                 # Processed files archive
└── README.md               # Setup and usage instructions
```

# DETAILED EXPLANATION:
- **adz.py**: Single-file Python application with UV dependencies and complete workflow engine
- **drops.yaml**: YAML configuration defining drop zones, file patterns, and agent assignments
- **prompts/**: Markdown templates with variable substitution for different workflow types
- **zones/**: Monitored directories where users drop files to trigger workflows
- **output/**: Organized storage for all generated assets and workflow results
- **archive/**: Automatic storage for processed input files after successful completion
- **echo.md**: Simple test workflow that echoes file contents back
- **create_image.md**: Workflow for generating images from text prompts using AI
- **edit_image.md**: Workflow for modifying existing images with AI editing
- **morning_debrief.md**: Audio transcription and analysis workflow for voice recordings
- **expand_training.md**: Data augmentation workflow for machine learning datasets
- **finance_categorize.md**: Automated categorization and analysis of financial data
- **README.md**: Comprehensive setup guide with configuration examples and usage instructions

# CODE:

## adz.py
```python
#!/usr/bin/env python3
"""
Agentic Drop Zone - File-based AI workflow automation system
Monitors directories for file drops and triggers AI agents to process them
"""

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "anthropic>=0.40.0",
#     "watchdog>=4.0.0",
#     "pyyaml>=6.0.1",
#     "rich>=13.7.0",
#     "openai>=1.0.0",
#     "google-generativeai>=0.8.0",
# ]
# ///

import os
import sys
import yaml
import asyncio
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import time

# Third-party imports
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.panel import Panel
import logging

# AI SDK imports
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Setup rich console and logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)

@dataclass
class DropZone:
    """Configuration for a drop zone"""
    name: str
    directory: str
    file_patterns: List[str]
    prompt_template: str
    agent: str = "claude"
    model: str = "claude-3-5-sonnet-20241022"
    color: str = "blue"
    events: List[str] = None
    
    def __post_init__(self):
        if self.events is None:
            self.events = ["created", "modified"]

@dataclass
class WorkflowResult:
    """Result of a workflow execution"""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0

class AgentManager:
    """Manages different AI agents and their execution"""
    
    def __init__(self):
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize AI service clients"""
        self.claude_client = None
        self.openai_client = None
        self.gemini_client = None
        
        # Setup Claude
        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.claude_client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        
        # Setup OpenAI
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        
        # Setup Gemini
        if GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    def build_prompt(self, template_path: str, file_path: str, **kwargs) -> str:
        """Build prompt from template with variable substitution"""
        try:
            with open(template_path, 'r') as f:
                template = f.read()
            
            # Replace common variables
            variables = {
                'drop_file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                **kwargs
            }
            
            # Simple variable substitution
            for key, value in variables.items():
                template = template.replace(f'{{{key}}}', str(value))
            
            return template
        except Exception as e:
            logger.error(f"Failed to build prompt: {e}")
            return ""
    
    def execute_claude(self, prompt: str, model: str = "claude-3-5-sonnet-20241022") -> WorkflowResult:
        """Execute workflow using Claude"""
        if not self.claude_client:
            return WorkflowResult(False, "", "Claude client not available")
        
        start_time = time.time()
        try:
            response = self.claude_client.messages.create(
                model=model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            execution_time = time.time() - start_time
            return WorkflowResult(
                True, 
                response.content[0].text,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return WorkflowResult(
                False, 
                "", 
                str(e),
                execution_time=execution_time
            )
    
    def execute_gemini_cli(self, prompt: str, model: str = "gemini-2.0-flash-exp") -> WorkflowResult:
        """Execute workflow using Gemini CLI"""
        start_time = time.time()
        try:
            # Use subprocess to call gemini CLI
            result = subprocess.run([
                "gemini", "chat",
                "--model", model,
                "--message", prompt
            ], capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                return WorkflowResult(
                    True,
                    result.stdout.strip(),
                    execution_time=execution_time
                )
            else:
                return WorkflowResult(
                    False,
                    "",
                    result.stderr.strip(),
                    execution_time=execution_time
                )
        except Exception as e:
            execution_time = time.time() - start_time
            return WorkflowResult(
                False,
                "",
                str(e),
                execution_time=execution_time
            )
    
    def execute_workflow(self, agent: str, prompt: str, model: str) -> WorkflowResult:
        """Execute workflow with specified agent"""
        logger.info(f"Executing workflow with {agent} using model {model}")
        
        if agent == "claude":
            return self.execute_claude(prompt, model)
        elif agent == "gemini":
            return self.execute_gemini_cli(prompt, model)
        else:
            return WorkflowResult(False, "", f"Unknown agent: {agent}")

class DropZoneHandler(FileSystemEventHandler):
    """Handles file system events for drop zones"""
    
    def __init__(self, drop_zones: List[DropZone], agent_manager: AgentManager, output_dir: str, archive_dir: str):
        self.drop_zones = drop_zones
        self.agent_manager = agent_manager
        self.output_dir = Path(output_dir)
        self.archive_dir = Path(archive_dir)
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Create output and archive directories
        self.output_dir.mkdir(exist_ok=True)
        self.archive_dir.mkdir(exist_ok=True)
    
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            self.handle_file_event(event.src_path, "created")
    
    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory:
            self.handle_file_event(event.src_path, "modified")
    
    def handle_file_event(self, file_path: str, event_type: str):
        """Process file events and trigger appropriate workflows"""
        file_path = Path(file_path)
        
        # Find matching drop zone
        for zone in self.drop_zones:
            if self.matches_zone(file_path, zone, event_type):
                logger.info(f"[{zone.color}]File {file_path.name} triggered {zone.name} workflow[/]", extra={"markup": True})
                
                # Execute workflow in thread pool
                self.executor.submit(self.execute_zone_workflow, zone, file_path)
                break
    
    def matches_zone(self, file_path: Path, zone: DropZone, event_type: str) -> bool:
        """Check if file matches zone criteria"""
        # Check if file is in zone directory
        zone_path = Path(zone.directory).resolve()
        try:
            file_path.resolve().relative_to(zone_path)
        except ValueError:
            return False
        
        # Check event type
        if event_type not in zone.events:
            return False
        
        # Check file patterns
        if zone.file_patterns:
            for pattern in zone.file_patterns:
                if file_path.match(pattern):
                    return True
            return False
        
        return True
    
    def execute_zone_workflow(self, zone: DropZone, file_path: Path):
        """Execute workflow for a specific zone"""
        try:
            # Build prompt from template
            prompt_path = Path("prompts") / zone.prompt_template
            if not prompt_path.exists():
                logger.error(f"Prompt template not found: {prompt_path}")
                return
            
            prompt = self.agent_manager.build_prompt(
                str(prompt_path),
                str(file_path),
                zone_name=zone.name,
                output_directory=str(self.output_dir / zone.name)
            )
            
            if not prompt:
                logger.error(f"Failed to build prompt for {zone.name}")
                return
            
            # Execute workflow
            with console.status(f"[{zone.color}]Executing {zone.name} workflow...[/]"):
                result = self.agent_manager.execute_workflow(zone.agent, prompt, zone.model)
            
            if result.success:
                logger.info(f"[green]✓[/] {zone.name} workflow completed in {result.execution_time:.2f}s", extra={"markup": True})
                
                # Save output
                self.save_workflow_output(zone, file_path, result.output)
                
                # Archive processed file
                self.archive_file(file_path, zone.name)
                
            else:
                logger.error(f"[red]✗[/] {zone.name} workflow failed: {result.error}", extra={"markup": True})
        
        except Exception as e:
            logger.error(f"Error executing {zone.name} workflow: {e}")
    
    def save_workflow_output(self, zone: DropZone, input_file: Path, output: str):
        """Save workflow output to appropriate directory"""
        output_dir = self.output_dir / zone.name
        output_dir.mkdir(exist_ok=True)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"{input_file.stem}_{timestamp}_output.md"
        
        # Create output content with metadata
        content = f"""# {zone.name.title()} Workflow Output

**Input File:** {input_file.name}
**Timestamp:** {datetime.now().isoformat()}
**Zone:** {zone.name}
**Agent:** {zone.agent}
**Model:** {zone.model}

---

{output}
"""
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        logger.info(f"Output saved to: {output_file}")
    
    def archive_file(self, file_path: Path, zone_name: str):
        """Move processed file to archive"""
        archive_zone_dir = self.archive_dir / zone_name
        archive_zone_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m
