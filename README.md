# Python Project Context for GitHub Copilot

Context and configuration files to guide GitHub Copilot for Python development with Pixi, pytest, behave, and Playwright.

## What's Included

- **AI_CONTEXT.md** - Vendor-neutral context for all AI coding assistants (single source of truth)
- **COPILOT_CONTEXT.md** - Global coding style, patterns, and conventions
- **PY_STYLE.md** - Python-specific style guide
- **TESTING_GUIDE.md** - Testing conventions (pytest, behave, Playwright)
- **TOOLS_PREFERENCES.md** - Tooling commands and environment setup
- **DB_GUIDE.md** - Database configuration (SQLite/Postgres)
- **PROMPT_TEMPLATES.md** - Reusable prompts for AI assistant
- **pyproject.toml** - Ruff (format + lint), MyPy configuration
- **pixi.toml** - Pixi tasks and dependencies
- **.editorconfig** - Editor formatting rules
- **tests/conftest.py** - Pytest fixtures template
- **src/your_package_name/db.py** - SQLAlchemy setup example

## How to Use

1. **Copy files to your project root** (or extract the zip)
2. **Replace placeholders:**
   - `your_package_name` → your actual package name in src/ directory and imports
   - `python-project-context` → your project name in pixi.toml (currently set to this repo's name as a working example)
   - `[Your Name]` → your name in LICENSE
   
   **Note:** This repository uses `python-project-context` as the project name to provide a working example. When using these files for your own project, do a find-and-replace to update it to your actual project name.
3. **Keep context files open in VS Code** while coding to maximize Copilot's awareness
4. **Install dependencies:**
   ```bash
   pixi install
   python -m playwright install --with-deps
   ```
5. **Run tasks:**
   ```bash
   pixi run fmt      # Format code
   pixi run lint     # Lint
   pixi run test     # Run tests
   pixi run ci       # All checks
   ```

## GitHub Copilot Tips

- **Open tabs matter:** Keep COPILOT_CONTEXT.md and relevant guides open while coding
- **Reference in prompts:** Mention "follow COPILOT_CONTEXT.md" in Copilot Chat
- **Add examples:** Place golden examples in `examples/` folder for Copilot to mirror
- **Use PROMPT_TEMPLATES.md:** Copy/paste prompts for consistent results

## Folder Structure (Optional)

These files work from the root, but you can optionally organize as:
- `.github/copilot-instructions.md` (GitHub-specific, but not required)
- Root level is fine and more flexible for non-GitHub repos

## License

MIT License - see LICENSE file
