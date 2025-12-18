## TECH_STACK

### Languages
- Natural Language - Primary language for prompt engineering and agent communication
- Markdown - Documentation and prompt formatting
- JSON - Output formatting for agent responses
- YAML - Alternative output formatting
- XML - Structural markup for prompt sections
- Bash - Command execution and scripting

### Frameworks & Libraries
- Claude Code - Anthropic's official CLI for Claude agent interactions
- MCP Server - Model Context Protocol for tool integration
- Replicate - Image generation service integration

### Tools & Platforms
- Claude Code - AI agent development and prompt execution
- Replicate - Image generation and AI model hosting
- CLI tools - Command-line interface for agent operations

### Services & APIs
- Replicate API - Image generation services
- Claude API - Large language model interactions

## CODE_SNIPPETS

### Snippet 1: Basic Workflow Prompt Structure
**Context**: Foundation structure for workflow-based agent prompts
**Timestamp**: Not specified

```markdown
# TITLE

## PURPOSE
Execute the workflow and report sections to understand the codebase and summarize your understanding.

## WORKFLOW
1. [Sequential task step 1]
2. [Sequential task step 2]

## REPORT
[Output format specifications]
```

**Explanation**: Basic three-section structure for agent prompts with input, workflow, and output
**Key Points**: Consistency in structure is crucial for agent understanding

### Snippet 2: Variable Syntax Implementation
**Context**: Dynamic and static variable handling in prompts
**Timestamp**: Not specified

```markdown
## VARIABLES
- user_prompt: {{ARGUMENT}} - The user's request or requirements
- plan_output_directory: specs - Static directory for output files
- image_count: {{ARG2}} - Number of images to generate
```

**Explanation**: Shows both dynamic variables (from arguments) and static variables (hardcoded values)
**Key Points**: Variables enable prompt reusability and parameterization

### Snippet 3: Control Flow Implementation
**Context**: Adding conditional logic and loops to agent workflows
**Timestamp**: Not specified

```markdown
## WORKFLOW
1. If no path to plan is provided, immediately stop and ask the user to provide it
2. Generate {{number_of_images}} images using the image generation prompt following the image loop below:

<image_loop>
- Use tool: replicate_image_generation
- Pass argument: {{image_prompt}}
- Use aspect ratio: {{aspect_ratio}}
- Wait for completion
</image_loop>
```

**Explanation**: Demonstrates conditional statements and loop structures within natural language workflows
**Key Points**: XML tags provide clear structure boundaries for complex operations

### Snippet 4: Agent Delegation Pattern
**Context**: Prompt that spawns multiple sub-agents for parallel processing
**Timestamp**: Not specified

```markdown
## WORKFLOW
1. Analyze the prompt request and determine optimal task division
2. Design agent prompts:
   - Create detailed self-contained prompts for each agent
   - Include specific instructions
   - Define clear output expectations
3. Launch {{count}} parallel agents with individual prompts
4. Monitor progress and collect results
5. Synthesize findings into final report
```

**Explanation**: Shows how to structure prompts that manage multiple agent instances
**Key Points**: Requires careful consideration of information flow between agents

## COMMANDS & SCRIPTS

### Installation & Setup
```bash
# No specific installation commands mentioned
```

### Configuration
```bash
# Environment variables for agent configuration
MODEL_NAME=[Specify model to use]
OUTPUT_DIRECTORY=[Path for output files]
```

### Execution & Testing
```bash
# Basic prompt execution
/prime

# Workflow prompt with arguments
/build path/to/plan

# Image generation with parameters
/create_image "image_prompts.txt" 5

# Parallel agent execution
/parallel "Extract information task" 5

# Background agent execution
/background task_description model_name report_file
```

### Deployment
```bash
# No specific deployment commands mentioned
```

## TECHNICAL_CONCEPTS

### Architectural Patterns
- **Input-Workflow-Output Pattern**: Three-step structure for all agent prompts - provides clear separation of concerns
- **Delegation Pattern**: Primary agent manages multiple sub-agents - enables parallel processing and task distribution
- **Template Meta Pattern**: Prompts that generate other prompts - scales prompt engineering capabilities

### Design Principles
- **Consistency Over Complexity**: Use standardized prompt formats to reduce confusion for agents, teams, and future self
- **Stakeholder Trifecta**: Design prompts for three audiences - you, your team, and your agents
- **Composable Sections**: Use interchangeable "Lego block" sections that can be swapped in and out as needed

### Best Practices
- **Direct Communication**: Use clear, dry language when addressing agents rather than conversational tone
- **Variable Referencing**: Implement consistent syntax for both static and dynamic variables throughout prompts
- **Section Minimalism**: Only include sections that are necessary - avoid adding unused components

### Common Pitfalls
- **Format Inconsistency**: Changing prompt structure between different prompts increases cognitive load and agent confusion
- **Over-complexity**: Adding unnecessary sections or overly complex workflows when simpler solutions suffice
- **Poor Variable Management**: Inconsistent variable naming or referencing patterns across prompts

## DEPENDENCIES & REQUIREMENTS

### System Requirements
- **Claude Code CLI**: Required for agent prompt execution
- **Command Line Interface**: For running agent commands and workflows

### Package Dependencies
- **MCP Server Integration**: For tool calling and external service integration
- **Replicate SDK**: For image generation capabilities

### Environment Variables
```bash
CLAUDE_API_KEY=[Your Claude API key]
REPLICATE_API_TOKEN=[Replicate service token for image generation]
OUTPUT_PATH=[Default output directory path]
MODEL_PREFERENCE=[Preferred model for agent execution]
```

### Prerequisites
- **Understanding of Agent Workflows**: Knowledge of how agents process sequential tasks
- **Prompt Engineering Fundamentals**: Basic understanding of how to communicate with AI agents
- **CLI Proficiency**: Ability to execute commands and manage files via command line

## RESOURCES & LINKS

### Official Documentation
- **Claude Code Documentation**: [URL not provided] - Official documentation for Claude Code CLI

### Repository Links
- **Agent Prompt Templates**: [URL not provided] - Repository containing the seven levels of prompt formats

### Related Tools & Extensions
- **TAC (The Agentic Course)**: [URL not provided] - Comprehensive course on agentic engineering
- **Elite Context Engineering**: [URL not provided] - Extended lesson on context management
- **Cloud Code SDK Mastery**: [URL not provided] - Course for building specialized agents

### Learning Resources
- **Agentic Prompt Engineering Guide**: [URL not provided] - Complete guide to the seven prompt levels
- **Context Engineering Framework**: [URL not provided] - R&D framework for context management

### Community & Support
- None identified

## CONFIGURATION_FILES

### claude.md
**Purpose**: Configuration file for agent knowledge and context
**Location**: Root directory of project

```markdown
# Claude Configuration
Essential information that all future agents should know about this codebase.

## Key Components
- [Component 1]: [Description]
- [Component 2]: [Description]

## Important Patterns
- [Pattern]: [Usage]
```

### prompt-template.md
**Purpose**: Template structure for creating new agent prompts
**Location**: Prompts directory

```markdown
# [PROMPT_TITLE]

## METADATA
- Description: [Brief description]
- Model: [Preferred model]
- Tools: [Allowed tools]

## PURPOSE
[Direct statement of what this prompt accomplishes]

## VARIABLES
- [variable_name]: {{ARGUMENT}} - [Description]
- [static_var]: [value] - [Purpose]

## WORKFLOW
1. [Step 1]
2. [Step 2]

## REPORT
[Output format specification]
```

## WORKFLOW_STEPS

### Setup Process
1. **Install Claude Code CLI** - Set up the primary agent interface
2. **Configure environment variables** - Set API keys and default paths
3. **Create prompt directory structure** - Organize prompts by complexity level
4. **Test basic prompt execution** - Verify agent communication works

### Development Workflow
1. **Start with Level 1 (Ad Hoc)** - Create simple, direct prompts for immediate needs
2. **Scale to Level 2 (Workflow)** - Add sequential steps when tasks become repetitive
3. **Add Level 3 (Control Flow)** - Implement conditionals and loops for complex logic
4. **Implement Level 4 (Delegation)** - Use multiple agents for parallel processing

### Testing & Validation
1. **Test prompt execution** - Run prompts with various inputs to verify behavior
2. **Validate variable handling** - Ensure both static and dynamic variables work correctly
3. **Check control flow** - Verify conditionals and loops execute as expected
4. **Monitor agent delegation** - Ensure sub-agents receive proper instructions

### Deployment Process
1. **Organize prompt library** - Structure prompts by use case and complexity
2. **Document prompt purposes** - Maintain clear descriptions for team usage
3. **Version control prompts** - Track changes and improvements over time
4. **Share with team** - Ensure consistent usage across team members

## AUTOMATION_OPPORTUNITIES

- **Prompt Template Generation**: Create scripts to generate new prompts based on common patterns and use cases
- **Variable Validation**: Automate checking that all referenced variables are properly defined in prompts
- **Prompt Testing Pipeline**: Automated testing of prompts with different input combinations to ensure reliability
- **Documentation Generation**: Auto-generate documentation from prompt metadata and structure
- **Performance Monitoring**: Track prompt execution times and success rates to identify optimization opportunities

## TECHNICAL_NOTES

### Performance Considerations
- **Token Efficiency**: Longer, more complex prompts consume more tokens but provide better agent guidance
- **Parallel Processing**: Delegation prompts can significantly speed up complex tasks through parallel agent execution
- **Context Management**: Static variables and codebase structure sections reduce token usage by providing upfront context

### Security Considerations
- **Input Validation**: Always validate user inputs, especially in delegation prompts that spawn multiple agents
- **Access Control**: Be mindful of what tools and capabilities you grant to different prompt levels
- **Output Sanitization**: Ensure agent outputs are properly formatted and don't contain harmful content

### Compatibility Notes
- **Model Variations**: Different models may interpret prompt structures differently - test across target models
- **Tool Integration**: MCP server compatibility required for external tool usage
- **CLI Version**: Ensure Claude Code CLI version supports all used features

### Troubleshooting Tips
- **Agent Not Following Workflow**: Check for inconsistent section formatting or unclear step descriptions
- **Variable Not Recognized**: Verify variable syntax matches the defined format ({{ARGUMENT}} for dynamic, plain text for static)
- **Control Flow Issues**: Ensure conditional statements use clear, unambiguous language
- **Delegation Failures**: Check that sub-agent prompts are self-contained and have all necessary context

## QUICK_REFERENCE

### Essential Commands
```bash
# Basic prompt execution
/[prompt_name]

# Prompt with single argument
/[prompt_name] "argument_value"

# Prompt with multiple arguments
/[prompt_name] "arg1" "arg2" "arg3"

# Background execution
/background "task" "model" "report_file"
```

### Key File Locations
- **Prompts Directory**: ./prompts/ - Contains all agent prompt files
- **Output Directory**: ./specs/ - Default location for agent-generated files
- **AI Documentation**: ./ai_docs/ - Agent-accessible documentation
- **Configuration**: ./claude.md - Agent knowledge base

### Important URLs
- **Claude Code Documentation**: [URL not provided]
- **TAC Course**: [URL not provided] 
- **Elite Context Engineering**: [URL not provided]
- **SDK Mastery Course**: [URL not provided]
