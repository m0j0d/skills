---
name: playwright
description: Browser automation for web debugging, testing, and inspection using Playwright. Navigate pages, take screenshots, read console logs, execute JavaScript, and interact with elements.
tags: [productivity, browser, testing, debugging, automation]
created_from: mcp-to-skill
last_validated: 2025-10-25
version: 1.0.0
---

# Playwright Skill

Browser automation and web debugging using Playwright. This skill provides direct access to browser capabilities without requiring vision models - uses structured accessibility snapshots and DOM inspection.

**Created from:** Microsoft Playwright MCP Server + ExecuteAutomation MCP Playwright

## When to Use This Skill

Use this skill when you need to:
- **Debug web applications** - See what's actually rendering, read console errors
- **Inspect local files** - Open file:/// URLs to debug local HTML/JS projects
- **Take screenshots** - Capture visual state of web pages
- **Execute JavaScript** - Run code in browser context to inspect state
- **Read console logs** - Get browser console output (errors, warnings, logs)
- **Interact with pages** - Click, fill forms, navigate

## Available Tools

### Navigation

**playwright_navigate** - Open a URL in the browser
```bash
python scripts/playwright_wrapper.py navigate --url "file:///C:/path/to/index.html" --headless
python scripts/playwright_wrapper.py navigate --url "https://example.com" --width 1920 --height 1080
```

Parameters:
- `url` (required) - URL to navigate to (supports file:// for local files)
- `--browser` - chromium, firefox, webkit (default: chromium)
- `--width` - Viewport width (default: 1280)
- `--height` - Viewport height (default: 720)
- `--headless` - Run without visible browser window
- `--timeout` - Navigation timeout in ms (default: 30000)

**playwright_go_back** / **playwright_go_forward** - Browser history navigation

### Inspection

**playwright_screenshot** - Capture page screenshot
```bash
python scripts/playwright_wrapper.py screenshot --name "debug" --fullPage
python scripts/playwright_wrapper.py screenshot --name "element" --selector "#app"
```

Parameters:
- `name` (required) - Filename for screenshot
- `--selector` - CSS selector to screenshot specific element
- `--fullPage` - Capture entire scrollable page
- `--savePng` - Save as PNG file to disk
- `--storeBase64` - Return base64 encoded image

**playwright_console_logs** - Read browser console messages
```bash
python scripts/playwright_wrapper.py console --type error
python scripts/playwright_wrapper.py console --search "Meadowcraft" --limit 50
```

Parameters:
- `--type` - Filter by: all, error, warning, log, info, debug (default: all)
- `--search` - Search term to filter messages
- `--limit` - Max number of messages to return
- `--clear` - Clear console after reading

**playwright_get_visible_text** - Extract visible text from page
```bash
python scripts/playwright_wrapper.py visible-text --selector ".error-message"
```

**playwright_get_visible_html** - Get page HTML
```bash
python scripts/playwright_wrapper.py visible-html --selector "#app" --cleanHtml
```

Parameters:
- `--selector` - CSS selector for specific element
- `--removeScripts` - Strip <script> tags
- `--removeStyles` - Strip <style> tags
- `--cleanHtml` - Remove comments, scripts, styles, meta tags

### Interaction

**playwright_click** - Click an element
```bash
python scripts/playwright_wrapper.py click --selector "button#start-game"
```

**playwright_fill** - Fill input field
```bash
python scripts/playwright_wrapper.py fill --selector "input[name='username']" --value "testuser"
```

**playwright_evaluate** - Execute JavaScript in browser
```bash
python scripts/playwright_wrapper.py evaluate --script "console.log(game.state.garden.plants.length)"
python scripts/playwright_wrapper.py evaluate --script "document.querySelector('#app').innerText"
```

Parameters:
- `script` (required) - JavaScript code to execute
- Returns evaluation result as JSON

### Common Workflows

#### Debug Local Web App
```bash
# 1. Open the local file
python scripts/playwright_wrapper.py navigate --url "file:///C:/projects/meadowcraft/index.html"

# 2. Read console errors
python scripts/playwright_wrapper.py console --type error

# 3. Take screenshot to see visual state
python scripts/playwright_wrapper.py screenshot --name "app-state" --fullPage --savePng

# 4. Inspect JavaScript state
python scripts/playwright_wrapper.py evaluate --script "JSON.stringify(game.state)"
```

#### Monitor Game State
```bash
# Check if plants are loading
python scripts/playwright_wrapper.py evaluate --script "game.state.garden.plants.length"

# Check database status
python scripts/playwright_wrapper.py evaluate --script "game.plantDatabase?.isLoaded"

# Get current plant types
python scripts/playwright_wrapper.py evaluate --script "JSON.stringify(game.state.garden.plants.map(p => p.type))"
```

## Installation

**Prerequisites:**
- Python 3.8+
- Node.js 18+ (for Playwright installation)

**Install Playwright:**
```bash
pip install playwright
playwright install chromium
```

## Bundled Scripts

- `scripts/playwright_wrapper.py` - Main tool wrapper with CLI interface
- `scripts/debug_webapp.py` - Helper script for common debugging workflows

## Implementation Notes

**Browser State:**
- Browser instances persist across commands within a session
- Use `--headless` for faster execution without GUI
- Default viewport: 1280x720 (customize with --width/--height)

**Local Files:**
- Use `file:///` protocol for local HTML files
- Windows paths: `file:///C:/path/to/file.html`
- Unix paths: `file:///home/user/file.html`

**Screenshot Storage:**
- Screenshots saved to current directory by default
- Use `--downloadsDir` to specify custom location
- Both PNG files and base64 encoding supported

**Console Logs:**
- Logs persist until cleared with `--clear`
- Filter by type (error, warning, etc.) for focused debugging
- Use `--search` for keyword filtering

## Security Considerations**⚠️ This skill is intended for LOCAL DEVELOPMENT and DEBUGGING only.**### Known Security Risks**1. Arbitrary JavaScript Execution**- The `evaluate` command executes user-provided JavaScript in browser context- **Only use with code you trust and understand**- Can access DOM, cookies, localStorage of visited pages- Never run untrusted scripts, especially after visiting unknown sites**2. Server-Side Request Forgery (SSRF)**- The `navigate` command can access any URL including:  - Internal network addresses (localhost, 192.168.x.x, 10.x.x.x)  - Cloud metadata endpoints (169.254.169.254)  - File system via file:// protocol- **Use caution when automating navigation to URLs from external sources****3. Path Traversal in Screenshots**- Screenshot filenames are not fully validated- **Use simple filenames without path separators (/, )**- Avoid: `../../../etc/file.png`- Safe: `my-screenshot.png`**4. Resource Exhaustion**- No built-in limits on script execution time or memory- Infinite loops or large pages can hang the browser- **Monitor browser resource usage during automation**### Safe Usage Guidelines✅ **Recommended Use Cases:**- Debugging your own web applications locally- Testing local HTML/JavaScript projects (file:// URLs)- Inspecting pages you control- Taking screenshots of trusted sites for documentation❌ **NOT Recommended:**- Automated scraping of untrusted websites- Processing URLs from user input in production- Running scripts provided by others without review- Exposing this tool via web API to untrusted users### Best Practices1. **Validate URLs** - Only navigate to sites you trust2. **Review scripts** - Read JavaScript code before executing via `evaluate`3. **Use headless mode** - Reduces GUI-based attack surface4. **Local development only** - Not designed for production web scraping5. **Monitor resources** - Watch for memory leaks in long-running sessions**Security Score:** 6/10 (Acceptable for informed users with local debugging use cases)
## Limitations

- Browser must be kept open between commands in same debugging session
- Screenshot of local files requires proper file:// URL format
- Some browser features (like WebGL) may behave differently in headless mode

## References

- Microsoft Playwright MCP: https://github.com/microsoft/playwright-mcp
- ExecuteAutomation MCP: https://github.com/executeautomation/mcp-playwright
- Playwright Docs: https://playwright.dev/python/
