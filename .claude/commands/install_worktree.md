# Install Worktree

This command sets up an isolated worktree environment with custom configuration.

## Parameters
- Worktree path: {0}
- Additional configuration: {1} (optional JSON string with custom env vars)

## Configuration Sources
The command will look for these files in the parent repo to copy:
- `.env.sample` or `.env` (root level)
- `.mcp.json` (MCP server configuration)
- `playwright-mcp-config.json` (Playwright automation config, if applicable)
- Any project-specific `.env.sample` files in subdirectories

## Steps

1. **Validate worktree path**
   ```bash
   cd {0}
   ```
   - Ensure the worktree directory exists and is accessible

2. **Create custom configuration file**
   If additional configuration is provided via parameter {1}:
   - Parse the JSON configuration
   - Create `.worktree.env` with the custom environment variables
   - This allows flexible per-worktree configuration without hardcoding port numbers or app-specific settings

3. **Copy and update environment files**
   - Copy `.env` from parent repo if it exists, otherwise use `.env.sample`
   - If `.worktree.env` was created, append its contents to `.env`
   - Recursively search for `**/.env.sample` files in parent repo and copy to equivalent paths
   - Update any relative paths in environment files to use absolute paths based on worktree location

4. **Copy and configure MCP files**
   ⚠️ **IMPORTANT**: These files should ONLY be created in the worktree directory, NEVER in the parent repository.
   The files contain hardcoded absolute paths specific to this worktree and will cause environment pollution if
   created in the main repo. Automated cleanup runs before worktree creation to prevent stale config files.

   - Copy `.mcp.json` from parent repo if it exists (as a template)
   - Copy `playwright-mcp-config.json` from parent repo if it exists (as a template)
   - These files enable Model Context Protocol and browser automation in the worktree

   After copying, update paths to use absolute paths for THIS worktree only:
   - Get the absolute worktree path: `WORKTREE_PATH=$(pwd)`
   - Update `.mcp.json`:
     - Find lines containing relative paths (e.g., `"./playwright-mcp-config.json"`)
     - Replace with absolute paths (e.g., `"${WORKTREE_PATH}/playwright-mcp-config.json"`)
     - Maintain valid JSON structure during replacement
   - Update `playwright-mcp-config.json`:
     - Find relative directory paths (e.g., `"dir": "./videos"`)
     - Replace with absolute paths (e.g., `"dir": "${WORKTREE_PATH}/videos"`)
     - Create required directories: `mkdir -p ${WORKTREE_PATH}/videos`
   - This ensures MCP configuration works correctly regardless of execution context

5. **Detect and install dependencies**
   Automatically detect the project type and install dependencies:

   - **Python projects** (if `pyproject.toml` or `requirements.txt` exists):
     ```bash
     uv sync --all-extras
     ```

   - **Node.js projects** (if `package.json` exists):
     ```bash
     npm install
     # or
     bun install
     # or
     yarn install
     ```
     (Use the package manager specified in the parent repo's configuration)

   - **Rust projects** (if `Cargo.toml` exists):
     ```bash
     cargo build
     ```

   - **Go projects** (if `go.mod` exists):
     ```bash
     go mod download
     ```

6. **Run project-specific setup scripts**
   Look for and execute setup scripts in this order (if they exist):
   - `./scripts/worktree_setup.sh`
   - `./scripts/setup.sh`
   - `./scripts/init_db.sh` or `./scripts/reset_db.sh`

   These scripts should be idempotent and safe to run in isolated worktrees.

7. **Validate installation**
   - Check that all dependency installation commands succeeded
   - Verify that required environment variables are set
   - Test that MCP configuration files have valid JSON syntax
   - Confirm that absolute paths in configuration files are correct

## Error Handling
- If parent environment files don't exist, create minimal versions from `.env.sample` files
- If no sample files exist, create an empty `.env` and log a warning
- Ensure all paths are absolute to avoid confusion across worktrees
- If dependency installation fails, log the error and continue with remaining steps
- Capture and report all errors in the final report

## Extensibility Hooks
This command supports project-specific customization through:
- **Custom configuration JSON**: Pass arbitrary env vars via parameter {1}
- **Setup scripts**: Place scripts in `./scripts/worktree_setup.sh` for automatic execution
- **Environment templates**: Define `.env.worktree.template` in parent repo for worktree-specific defaults

## Report
After completion, provide a structured report including:
- List all files created/modified (including MCP configuration files)
- Show custom configuration applied (if any)
- List dependencies installed per detected project type
- Confirm setup scripts executed (if any)
- Note any missing parent files that need user attention
- Note any missing MCP configuration files
- Show the updated absolute paths in:
  - `.mcp.json` (should show full paths)
  - `playwright-mcp-config.json` (should show full path to videos directory)
- Confirm required directories were created (e.g., videos/)
- List any errors or warnings encountered
- Provide next steps for the user (e.g., "Run `cd {0} && npm start` to start development")

## Example Usage

Basic installation:
```
/install_worktree /path/to/worktree
```

With custom configuration:
```
/install_worktree /path/to/worktree '{"API_PORT": "8080", "DEBUG": "true"}'
```
