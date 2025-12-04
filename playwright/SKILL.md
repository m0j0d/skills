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

**browser_navigate** - Navigate to a URL
```bash
python scripts/browser_tools.py browser_navigate --url "file:///C:/path/to/index.html"
python scripts/browser_tools.py browser_navigate --url "https://example.com" --timeout 30000
```

Parameters:
- `url` (required) - URL to navigate to (supports file:// for local files)
- `timeout` - Navigation timeout in ms (default: 30000)

**browser_navigate_back** - Go back to the previous page

**browser_close** - Close the browser

### Inspection

**browser_screenshot** - Take a screenshot of the current page
```bash
python scripts/browser_tools.py browser_screenshot --filename "debug.png" --fullPage true
python scripts/browser_tools.py browser_screenshot --ref "#app"
```

Parameters:
- `filename` - Save location (optional, returns base64 if not provided)
- `fullPage` - Capture entire scrollable page (default: false)
- `ref` - CSS selector for specific element

**browser_console_messages** - Returns all console messages
```bash
python scripts/browser_tools.py browser_console_messages --onlyErrors true
```

Parameters:
- `onlyErrors` - Filter for errors only (default: false)

**browser_snapshot** - Capture accessibility snapshot of the current page

**browser_evaluate** - Evaluate JavaScript expression on page
```bash
python scripts/browser_tools.py browser_evaluate --function "game.state.garden.plants.length"
python scripts/browser_tools.py browser_evaluate --function "document.title"
```

Parameters:
- `function` (required) - JavaScript code to execute
- `ref` - CSS selector for element context (optional)

### Interaction

**browser_click** - Perform click on a web page
```bash
python scripts/browser_tools.py browser_click --element "start button" --ref "button#start-game"
```

Parameters:
- `element` - Human-readable element description
- `ref` (required) - CSS selector for target element
- `doubleClick` - Double click toggle (default: false)
- `button` - Mouse button: left, right, middle (default: left)

**browser_type** - Type text into editable element
```bash
python scripts/browser_tools.py browser_type --element "username field" --ref "input[name='username']" --text "testuser"
```

Parameters:
- `element` - Element description
- `ref` (required) - CSS selector for input element
- `text` (required) - Text content to type
- `submit` - Press Enter after typing (default: false)
- `slowly` - Type character by character (default: false)

**browser_hover** - Hover over element on page

**browser_select_option** - Select an option in a dropdown

**browser_press_key** - Press a key on the keyboard

**browser_wait_for** - Wait for text or time delay
```bash
python scripts/browser_tools.py browser_wait_for --time 2
python scripts/browser_tools.py browser_wait_for --text "Loading complete"
```

Parameters:
- `time` - Wait duration in seconds
- `text` - Text to appear
- `textGone` - Text to disappear

**browser_resize** - Resize the browser window

### Common Workflows

#### Debug Local Web App
```bash
# 1. Open the local file
python scripts/browser_tools.py browser_navigate --url "file:///C:/projects/meadowcraft/index.html"

# 2. Read console errors
python scripts/browser_tools.py browser_console_messages --onlyErrors true

# 3. Take screenshot to see visual state
python scripts/browser_tools.py browser_screenshot --filename "app-state.png" --fullPage true

# 4. Inspect JavaScript state
python scripts/browser_tools.py browser_evaluate --function "JSON.stringify(game.state)"
```

#### Monitor Game State
```bash
# Check if plants are loading
python scripts/browser_tools.py browser_evaluate --function "game.state.garden.plants.length"

# Check database status
python scripts/browser_tools.py browser_evaluate --function "game.plantDatabase?.isLoaded"

# Get current plant types
python scripts/browser_tools.py browser_evaluate --function "JSON.stringify(game.state.garden.plants.map(p => p.type))"
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

- `scripts/browser_tools.py` - Main browser automation tools with CLI interface

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
