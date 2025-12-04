#!/usr/bin/env python3
"""
Browser automation tools using Playwright.
Implements browser_* functions matching the playwright-mcp MCP server.

This is a STATEFUL module - browser context persists between calls.
"""

import asyncio
import json
import sys
import re
from typing import Dict, List, Any, Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext


# Global state for browser session
_playwright = None
_browser: Optional[Browser] = None
_context: Optional[BrowserContext] = None
_page: Optional[Page] = None
_console_logs: List[Dict[str, Any]] = []


async def _ensure_browser(headless: bool = True, width: int = 1280, height: int = 720) -> Page:
    """Ensure browser is started and return page."""
    global _playwright, _browser, _context, _page, _console_logs

    if _page is None:
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(headless=headless)
        _context = await _browser.new_context(viewport={'width': width, 'height': height})
        _page = await _context.new_page()
        _console_logs = []

        # Capture console messages
        def on_console(msg):
            _console_logs.append({
                'type': msg.type,
                'text': msg.text,
                'location': str(msg.location)
            })
        _page.on('console', on_console)

    return _page


async def _run_async(coro):
    """Run async coroutine, creating event loop if needed."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return await coro
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


# Core Navigation Tools

def browser_navigate(url: str, timeout: int = 30000) -> Dict[str, Any]:
    """
    Navigate to a URL.

    Args:
        url: Target URL (supports file:// for local files)
        timeout: Navigation timeout in milliseconds

    Returns:
        Result with current URL and title
    """
    async def _navigate():
        page = await _ensure_browser()
        await page.goto(url, timeout=timeout, wait_until='load')
        return {
            'url': page.url,
            'title': await page.title()
        }

    return asyncio.run(_navigate())


def browser_close() -> Dict[str, Any]:
    """
    Close the browser.

    Returns:
        Success status
    """
    global _playwright, _browser, _context, _page, _console_logs

    async def _close():
        global _playwright, _browser, _context, _page
        if _browser:
            await _browser.close()
        if _playwright:
            await _playwright.stop()
        _browser = None
        _context = None
        _page = None
        _console_logs.clear()
        return {'status': 'closed'}

    return asyncio.run(_close())


def browser_navigate_back() -> Dict[str, Any]:
    """
    Go back to the previous page.

    Returns:
        Current URL after navigation
    """
    async def _back():
        page = await _ensure_browser()
        await page.go_back()
        return {'url': page.url}

    return asyncio.run(_back())


# Inspection Tools

def browser_screenshot(filename: str = '', fullPage: bool = False,
                       element: str = '', ref: str = '') -> Dict[str, Any]:
    """
    Take a screenshot of the current page.

    Args:
        filename: Save location (optional)
        fullPage: Capture entire scrollable page
        element: Element description (unused, for API compatibility)
        ref: CSS selector for specific element

    Returns:
        Screenshot path or base64 data
    """
    async def _screenshot():
        page = await _ensure_browser()

        options = {'full_page': fullPage}

        if ref:
            # Screenshot specific element
            element_handle = await page.query_selector(ref)
            if element_handle:
                if filename:
                    await element_handle.screenshot(path=filename)
                    return {'path': filename}
                else:
                    data = await element_handle.screenshot()
                    import base64
                    return {'base64': base64.b64encode(data).decode()}

        if filename:
            await page.screenshot(path=filename, **options)
            return {'path': filename}
        else:
            data = await page.screenshot(**options)
            import base64
            return {'base64': base64.b64encode(data).decode()}

    return asyncio.run(_screenshot())


def browser_console_messages(onlyErrors: bool = False) -> Dict[str, Any]:
    """
    Returns all console messages.

    Args:
        onlyErrors: Filter for errors only

    Returns:
        List of console messages
    """
    if onlyErrors:
        filtered = [log for log in _console_logs if log['type'] == 'error']
    else:
        filtered = _console_logs

    return {'messages': filtered, 'count': len(filtered)}


def browser_evaluate(function: str, element: str = '', ref: str = '') -> Dict[str, Any]:
    """
    Evaluate JavaScript expression on page or element.

    Args:
        function: JavaScript code to execute
        element: Element description (unused)
        ref: CSS selector for element context

    Returns:
        Evaluation result
    """
    async def _evaluate():
        page = await _ensure_browser()

        if ref:
            elem = await page.query_selector(ref)
            if elem:
                result = await elem.evaluate(function)
            else:
                return {'error': f'Element not found: {ref}'}
        else:
            result = await page.evaluate(function)

        return {'result': result}

    return asyncio.run(_evaluate())


def browser_snapshot() -> Dict[str, Any]:
    """
    Capture accessibility snapshot of the current page.

    Returns:
        Accessibility tree snapshot
    """
    async def _snapshot():
        page = await _ensure_browser()
        snapshot = await page.accessibility.snapshot()
        return {'snapshot': snapshot}

    return asyncio.run(_snapshot())


# Interaction Tools

def browser_click(element: str, ref: str, doubleClick: bool = False,
                  button: str = 'left', modifiers: List = None) -> Dict[str, Any]:
    """
    Perform click on a web page.

    Args:
        element: Human-readable element description (unused)
        ref: CSS selector for target element
        doubleClick: Double click toggle
        button: Mouse button (left, right, middle)
        modifiers: Modifier keys

    Returns:
        Success status
    """
    async def _click():
        page = await _ensure_browser()

        click_count = 2 if doubleClick else 1
        await page.click(ref, button=button, click_count=click_count)

        return {'status': 'clicked', 'selector': ref}

    return asyncio.run(_click())


def browser_type(element: str, ref: str, text: str,
                 submit: bool = False, slowly: bool = False) -> Dict[str, Any]:
    """
    Type text into editable element.

    Args:
        element: Element description (unused)
        ref: CSS selector for input element
        text: Text content to type
        submit: Press Enter after typing
        slowly: Type character by character

    Returns:
        Success status
    """
    async def _type():
        page = await _ensure_browser()

        if slowly:
            await page.type(ref, text, delay=100)
        else:
            await page.fill(ref, text)

        if submit:
            await page.press(ref, 'Enter')

        return {'status': 'typed', 'selector': ref}

    return asyncio.run(_type())


def browser_hover(element: str, ref: str) -> Dict[str, Any]:
    """
    Hover over element on page.

    Args:
        element: Element description (unused)
        ref: CSS selector for element

    Returns:
        Success status
    """
    async def _hover():
        page = await _ensure_browser()
        await page.hover(ref)
        return {'status': 'hovered', 'selector': ref}

    return asyncio.run(_hover())


def browser_select_option(element: str, ref: str, values: List) -> Dict[str, Any]:
    """
    Select an option in a dropdown.

    Args:
        element: Element description (unused)
        ref: CSS selector for select element
        values: Values to select

    Returns:
        Selected values
    """
    async def _select():
        page = await _ensure_browser()
        selected = await page.select_option(ref, values)
        return {'selected': selected}

    return asyncio.run(_select())


def browser_press_key(key: str) -> Dict[str, Any]:
    """
    Press a key on the keyboard.

    Args:
        key: Key name or character

    Returns:
        Success status
    """
    async def _press():
        page = await _ensure_browser()
        await page.keyboard.press(key)
        return {'status': 'pressed', 'key': key}

    return asyncio.run(_press())


def browser_wait_for(time: float = 0, text: str = '', textGone: str = '') -> Dict[str, Any]:
    """
    Wait for text or time delay.

    Args:
        time: Wait duration in seconds
        text: Text to appear
        textGone: Text to disappear

    Returns:
        Success status
    """
    async def _wait():
        page = await _ensure_browser()

        if time > 0:
            await asyncio.sleep(time)

        if text:
            await page.wait_for_selector(f'text={text}')

        if textGone:
            await page.wait_for_selector(f'text={textGone}', state='hidden')

        return {'status': 'waited'}

    return asyncio.run(_wait())


def browser_resize(width: int, height: int) -> Dict[str, Any]:
    """
    Resize the browser window.

    Args:
        width: Window width in pixels
        height: Window height in pixels

    Returns:
        New viewport size
    """
    async def _resize():
        page = await _ensure_browser()
        await page.set_viewport_size({'width': width, 'height': height})
        return {'width': width, 'height': height}

    return asyncio.run(_resize())


# ============================================================================
# NOT YET IMPLEMENTED - Stubs for remaining MCP server tools
# ============================================================================

def browser_drag(startElement: str, startRef: str, endElement: str, endRef: str) -> Dict[str, Any]:
    """Perform drag and drop between two elements."""
    raise NotImplementedError('browser_drag requires implementation')


def browser_file_upload(paths: List = None) -> Dict[str, Any]:
    """Upload one or multiple files."""
    raise NotImplementedError('browser_file_upload requires implementation')


def browser_fill_form(fields: List) -> Dict[str, Any]:
    """Fill multiple form fields."""
    raise NotImplementedError('browser_fill_form requires implementation')


def browser_generate_locator(element: str, ref: str) -> Dict[str, Any]:
    """Generate locator for the given element to use in tests."""
    raise NotImplementedError('browser_generate_locator requires implementation')


def browser_handle_dialog(accept: bool, promptText: str = '') -> Dict[str, Any]:
    """Handle a dialog."""
    raise NotImplementedError('browser_handle_dialog requires implementation')


def browser_install() -> Dict[str, Any]:
    """Install the browser specified in the config."""
    raise NotImplementedError('browser_install requires implementation')


def browser_mouse_click_xy(element: str, x: float, y: float) -> Dict[str, Any]:
    """Click left mouse button at a given position."""
    raise NotImplementedError('browser_mouse_click_xy requires implementation')


def browser_mouse_drag_xy(element: str, startX: float, startY: float, endX: float, endY: float) -> Dict[str, Any]:
    """Drag left mouse button to a given position."""
    raise NotImplementedError('browser_mouse_drag_xy requires implementation')


def browser_mouse_move_xy(element: str, x: float, y: float) -> Dict[str, Any]:
    """Move mouse to a given position."""
    raise NotImplementedError('browser_mouse_move_xy requires implementation')


def browser_network_requests() -> Dict[str, Any]:
    """Returns all network requests since loading the page."""
    raise NotImplementedError('browser_network_requests requires implementation')


def browser_pdf_save(filename: str = '') -> Dict[str, Any]:
    """Save page as PDF."""
    raise NotImplementedError('browser_pdf_save requires implementation')


def browser_run_code(code: str) -> Dict[str, Any]:
    """Run Playwright code snippet."""
    raise NotImplementedError('browser_run_code requires implementation')


def browser_start_tracing() -> Dict[str, Any]:
    """Start trace recording."""
    raise NotImplementedError('browser_start_tracing requires implementation')


def browser_stop_tracing() -> Dict[str, Any]:
    """Stop trace recording."""
    raise NotImplementedError('browser_stop_tracing requires implementation')


def browser_tabs(action: str, index: int = 0) -> Dict[str, Any]:
    """List, create, close, or select a browser tab."""
    raise NotImplementedError('browser_tabs requires implementation')


def browser_verify_element_visible(role: str, accessibleName: str) -> Dict[str, Any]:
    """Verify element is visible on the page."""
    raise NotImplementedError('browser_verify_element_visible requires implementation')


def browser_verify_list_visible(element: str, ref: str, items: List) -> Dict[str, Any]:
    """Verify list is visible on the page."""
    raise NotImplementedError('browser_verify_list_visible requires implementation')


def browser_verify_text_visible(text: str) -> Dict[str, Any]:
    """Verify text is visible on the page."""
    raise NotImplementedError('browser_verify_text_visible requires implementation')


def browser_verify_value(type: str, element: str, ref: str, value: str) -> Dict[str, Any]:
    """Verify element value."""
    raise NotImplementedError('browser_verify_value requires implementation')


# CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python browser_tools.py <tool_name> [--param value ...]")
        print("\nAvailable tools:")
        print("  browser_navigate: Navigate to a URL")
        print("  browser_close: Close the browser")
        print("  browser_screenshot: Take a screenshot")
        print("  browser_console_messages: Get console logs")
        print("  browser_evaluate: Execute JavaScript")
        print("  browser_click: Click an element")
        print("  browser_type: Type text into element")
        print("  browser_wait_for: Wait for condition")
        sys.exit(1)

    tool_name = sys.argv[1]

    # Parse parameters
    params = {}
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith('--'):
            param_name = sys.argv[i][2:]
            if i + 1 < len(sys.argv):
                value = sys.argv[i + 1]
                # Try to parse as JSON for complex types
                try:
                    value = json.loads(value)
                except:
                    pass
                params[param_name] = value
                i += 2
            else:
                print(f"Error: Missing value for parameter {param_name}")
                sys.exit(1)
        else:
            i += 1

    # Execute tool
    try:
        tool_func = globals().get(tool_name)
        if tool_func and callable(tool_func):
            result = tool_func(**params)
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"Error: Unknown tool '{tool_name}'")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
