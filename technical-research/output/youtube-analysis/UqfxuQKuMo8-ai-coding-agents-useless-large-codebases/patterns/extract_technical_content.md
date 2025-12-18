# TECH_STACK

### Languages
- C# - Primary language for refactoring examples and MCP server implementation
- TypeScript - Mentioned in codebase analysis (842,000 lines)

### Frameworks & Libraries
- .NET - Framework for C# development and Roslyn analyzers
- Roslyn - Microsoft's compiler platform used for C# code analysis and refactoring

### Tools & Platforms
- Claude Code - Anthropic's official CLI for Claude AI coding assistant
- Rider - JetBrains IDE with refactoring support
- Visual Studio Code - Code editor
- GitHub - Source code hosting and repository management
- cloc (Count Lines of Code) - Tool for counting lines of code in projects

### Services & APIs
- Anthropic Claude - AI coding assistant and language model
- MCP (Model Context Protocol) - Protocol for connecting AI assistants with external tools

## CODE_SNIPPETS

### Snippet 1: Timer and benchmark setup
**Context**: Setting up performance measurement for refactoring tasks
**Timestamp**: 02:22

```bash
# Starting timer for benchmark comparison
# Manual refactoring: 12 minutes baseline
# AI with tools: Target sub-6 minutes
```

**Explanation**: Establishes baseline performance metrics for comparing manual vs AI-assisted refactoring
**Key Points**: Manual approach took 12 minutes, AI with proper tools completed in 6 minutes (2x improvement)

### Snippet 2: Codebase analysis
**Context**: Analyzing the Umbraco CMS codebase size and complexity
**Timestamp**: 07:35

```bash
cloc .
# Results:
# 55,000 total files
# 842,000 TypeScript files  
# 360,000 lines of C#
```

**Explanation**: Demonstrates the scale of the test codebase used for benchmarking
**Key Points**: Large enough codebase to show meaningful performance differences between approaches

### Snippet 3: Rename refactoring command
**Context**: Using IDE built-in refactoring tools for baseline measurement
**Timestamp**: 08:25

```csharp
// Renaming GlobalSettings type across entire codebase
// IDE found and changed 147 files
// Took approximately 3 minutes including test execution
```

**Explanation**: Manual refactoring using IDE tools as performance baseline
**Key Points**: IDE refactoring is fast but requires manual intervention and verification

## COMMANDS & SCRIPTS

### Installation & Setup
```bash
# Install Serena MCP server
npm install -g serena-mcp

# Install Refactor MCP server (for .NET)
dotnet tool install -g refactor-mcp
```

### Configuration
```bash
# Add MCP server to Claude configuration
# Configure in claude.md or system prompt:
"Use the refactor MCP server for all refactoring operations"
```

### Execution & Testing
```bash
# Run unit tests after refactoring
dotnet test

# Build entire solution
dotnet build
```

### Deployment
```bash
# Standard .NET deployment commands
dotnet publish
```

## TECHNICAL_CONCEPTS

### Architectural Patterns
- **MCP (Model Context Protocol)**: Protocol for connecting AI assistants with external tools - Enables AI agents to use specialized tools rather than brute-force approaches
- **Semantic Search and Edit**: Advanced code navigation using meaning rather than text matching - More efficient than grep-based searches in large codebases

### Design Principles
- **Tool-First Approach**: Give AI agents proper tools before expecting good performance - Like "using a fork instead of a spoon for spaghetti"
- **Incremental Refactoring**: Break down large refactoring tasks into smaller, manageable steps

### Best Practices
- **Always run tests**: Include test execution as part of any refactoring workflow to ensure correctness
- **Use semantic tools**: Prefer AST-based and semantic tools over text-based manipulation for code changes
- **Measure performance**: Track token usage and time to optimize AI agent efficiency

### Common Pitfalls
- **Brute force approach**: Using basic Claude without specialized tools leads to doom loops and excessive token usage
- **Ignoring test feedback**: Not validating changes can lead to broken code that requires multiple fix iterations

## DEPENDENCIES & REQUIREMENTS

### System Requirements
- **.NET SDK**: Required for C# refactoring tools and compilation
- **Node.js**: Required for Serena MCP server installation

### Package Dependencies
- **Serena MCP**: Semantic search and edit capabilities
- **Refactor MCP**: Roslyn-based refactoring tools for .NET
- **Claude Code CLI**: Anthropic's official CLI tool

### Environment Variables
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

### Prerequisites
- **Large codebase**: Tools show most benefit on codebases with 100k+ lines of code
- **Test suite**: Essential for validating refactoring operations
- **Build system**: Automated compilation to catch errors quickly

## RESOURCES & LINKS

### Official Documentation
- **Serena MCP**: https://github.com/serena-ai/serena-mcp
- **Claude Code**: https://github.com/anthropics/claude-code

### Repository Links
- **Serena**: https://github.com/serena-ai/serena - Semantic code retrieval and editing tools
- **Refactor MCP**: https://github.com/davehillier/refactor-mcp - Roslyn-based refactoring tools for C#
- **Umbraco CMS**: https://github.com/umbraco/umbraco-cms - Test codebase used for benchmarking

### Related Tools & Extensions
- **MCP Servers**: Various language-specific servers available on GitHub
- **Roslyn Analyzers**: Microsoft's code analysis platform for .NET

### Learning Resources
- **MCP Protocol Documentation**: Learn how to build and configure MCP servers
- **Anthropic Claude Documentation**: Official guides for using Claude effectively

### Community & Support
- **GitHub Issues**: Primary support channel for MCP servers
- **Anthropic Discord**: Community discussions about Claude usage

## CONFIGURATION_FILES

### claude.md
**Purpose**: Configure Claude Code with MCP servers and system prompts
**Location**: Project root or user configuration directory

```markdown
# Claude Configuration
Use Serena MCP server for semantic code operations.
Use Refactor MCP server for all refactoring tasks.
Always run unit tests after making code changes.
```

### MCP Server Configuration
**Purpose**: Configure available MCP servers for Claude
**Location**: Claude configuration directory

```json
{
  "mcpServers": {
    "serena": {
      "command": "serena-mcp",
      "args": ["--workspace", "."]
    },
    "refactor": {
      "command": "refactor-mcp",
      "args": ["--solution", "*.sln"]
    }
  }
}
```

## WORKFLOW_STEPS

### Setup Process
1. Install required MCP servers (Serena, Refactor MCP)
2. Configure Claude with MCP server connections
3. Verify MCP servers are running and accessible
4. Test with small refactoring operation

### Development Workflow
1. Identify refactoring or code change requirement
2. Use semantic search to understand codebase structure
3. Plan refactoring steps using AI agent
4. Execute refactoring using appropriate MCP tools
5. Validate changes with automated tests

### Testing & Validation
1. Run unit tests after each refactoring step
2. Perform full solution build to catch compilation errors
3. Review changed files for correctness
4. Commit changes with descriptive messages

### Deployment Process
1. Ensure all tests pass
2. Build release configuration
3. Deploy using standard CI/CD pipeline
4. Monitor for any runtime issues

## AUTOMATION_OPPORTUNITIES

- **Refactoring workflows**: Create scripts that combine multiple refactoring operations with test validation
- **Code quality checks**: Automate running analyzers and formatters after AI-generated changes
- **Performance monitoring**: Track token usage and execution time across different approaches
- **Batch operations**: Process multiple similar refactoring tasks across different projects

## TECHNICAL_NOTES

### Performance Considerations
- **Token usage**: MCP servers reduce token consumption by 20-30x compared to brute force approaches
- **Execution time**: 30x faster execution with proper tools vs basic Claude usage
- **Memory usage**: Large codebases require sufficient RAM for semantic indexing

### Security Considerations
- **API key management**: Secure storage of Anthropic API keys
- **Code access**: MCP servers require file system access to codebase
- **Network security**: Some MCP servers may require network access

### Compatibility Notes
- **Language support**: Different MCP servers available for different programming languages
- **IDE integration**: Some tools work better with specific IDEs (e.g., Rider for .NET)
- **Version compatibility**: Ensure MCP server versions match your development tools

### Troubleshooting Tips
- **MCP server not found**: Check installation and PATH configuration
- **Slow performance**: Verify adequate system resources for large codebase analysis
- **Token limits**: Monitor usage to avoid hitting API rate limits
- **Build failures**: Always validate changes with automated tests

## QUICK_REFERENCE

### Essential Commands
```bash
# Check MCP server status
claude-code --list-servers

# Start refactoring session with timer
time claude-code --prompt "refactor-prompt.txt"

# Validate changes
dotnet test && dotnet build
```

### Key File Locations
- **MCP Configuration**: `~/.config/claude/mcp-servers.json` - MCP server definitions
- **Project Configuration**: `./claude.md` - Project-specific Claude settings
- **Test Results**: `./TestResults/` - Automated test output

### Important URLs
- **Serena Documentation**: https://github.com/serena-ai/serena
- **MCP Protocol Spec**: https://anthropic.com/mcp
- **Claude Code CLI**: https://github.com/anthropics/claude-code
