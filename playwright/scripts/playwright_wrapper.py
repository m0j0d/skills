#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Playwright Web Automation Wrapper
Provides browser automation tools from Playwright MCP servers
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright, Browser, Page, BrowserContext


class PlaywrightSession:
    """Manages a persistent Playwright browser session"""

    def __init__(self):
        self.playwright = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self.console_messages = []

    async def start(self, browser_type='chromium', headless=True, width=1280, height=720):
        """Initialize browser session"""
        if self.playwright is None:
            self.playwright = await async_playwright().start()

        if browser_type == 'chromium':
            browser_launcher = self.playwright.chromium
        elif browser_type == 'firefox':
            browser_launcher = self.playwright.firefox
        elif browser_type == 'webkit':
            browser_launcher = self.playwright.webkit
        else:
            raise ValueError(f"Unknown browser type: {browser_type}")

        self.browser = await browser_launcher.launch(headless=headless)
        self.context = await self.browser.new_context(
            viewport={'width': width, 'height': height}
        )
        self.page = await self.context.new_page()

        # Capture console messages
        self.page.on('console', lambda msg: self.console_messages.append({
            'type': msg.type,
            'text': msg.text,
            'location': msg.location
        }))

        return self.page

    async def close(self):
        """Close browser session"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def navigate(self, url, timeout=30000, wait_until='load'):
        """Navigate to URL"""
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.goto(url, timeout=timeout, wait_until=wait_until)
        return {
            'url': self.page.url,
            'title': await self.page.title()
        }

    async def screenshot(self, name, selector=None, full_page=False, save_png=True):
        """Take screenshot"""
        if not self.page:
            raise RuntimeError("Browser not started")

        path = f"{name}.png" if save_png else None

        if selector:
            element = await self.page.query_selector(selector)
            if not element:
                raise ValueError(f"Element not found: {selector}")
            screenshot_bytes = await element.screenshot(path=path)
        else:
            screenshot_bytes = await self.page.screenshot(
                path=path,
                full_page=full_page
            )

        return {
            'path': str(path) if path else None,
            'size': len(screenshot_bytes)
        }

    def get_console_logs(self, log_type='all', search=None, limit=None, clear=False):
        """Get console messages"""
        messages = self.console_messages

        # Filter by type
        if log_type != 'all':
            messages = [m for m in messages if m['type'] == log_type]

        # Filter by search term
        if search:
            messages = [m for m in messages if search.lower() in m['text'].lower()]

        # Limit results
        if limit:
            messages = messages[:limit]

        # Clear if requested
        if clear:
            self.console_messages.clear()

        return messages

    async def evaluate(self, script):
        """
        Execute JavaScript in the browser context and return result.
        
        **SECURITY WARNING**: This function executes arbitrary JavaScript code
        in the browser context. Only use with trusted input.
        
        NEVER expose this function to untrusted user input as it enables:
        - Arbitrary code execution in browser
        - Access to page content and DOM
        - Potential data exfiltration
        
        Args:
            script: JavaScript code to execute (MUST be from trusted source)
            
        Returns:
            Result of the JavaScript execution
            
        Raises:
            RuntimeError: If browser is not started
        """
        if not self.page:
            raise RuntimeError("Browser not started")

        result = await self.page.evaluate(script)
        return result

    async def click(self, selector, timeout=30000):
        """Click an element"""
        if not self.page:
            raise RuntimeError("Browser not started")

        await self.page.click(selector, timeout=timeout)
        return {'clicked': selector}

    async def fill(self, selector, value, timeout=30000):
        """Fill an input field"""
        if not self.page:
            raise RuntimeError("Browser not started")

        await self.page.fill(selector, value, timeout=timeout)
        return {'filled': selector, 'value': value}

    async def get_visible_text(self, selector=None):
        """Get visible text from page or element"""
        if not self.page:
            raise RuntimeError("Browser not started")

        if selector:
            element = await self.page.query_selector(selector)
            if not element:
                raise ValueError(f"Element not found: {selector}")
            text = await element.inner_text()
        else:
            text = await self.page.inner_text('body')

        return text

    async def get_visible_html(self, selector=None, clean_html=False):
        """Get HTML from page or element"""
        if not self.page:
            raise RuntimeError("Browser not started")

        if selector:
            element = await self.page.query_selector(selector)
            if not element:
                raise ValueError(f"Element not found: {selector}")
            html = await element.inner_html()
        else:
            html = await self.page.content()

        if clean_html:
            # Remove scripts, styles, comments
            script = """
            (html) => {
                const div = document.createElement('div');
                div.innerHTML = html;
                div.querySelectorAll('script, style, meta').forEach(el => el.remove());
                return div.innerHTML;
            }
            """
            html = await self.page.evaluate(script, html)

        return html

    async def go_back(self):
        """Navigate back in history"""
        if not self.page:
            raise RuntimeError("Browser not started")
        await self.page.go_back()
        return {'url': self.page.url}

    async def go_forward(self):
        """Navigate forward in history"""
        if not self.page:
            raise RuntimeError("Browser not started")
        await self.page.go_forward()
        return {'url': self.page.url}


# Global session for CLI usage
session = PlaywrightSession()


async def main():
    parser = argparse.ArgumentParser(description='Playwright Browser Automation')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Navigate command
    nav_parser = subparsers.add_parser('navigate', help='Navigate to URL')
    nav_parser.add_argument('--url', required=True, help='URL to navigate to')
    nav_parser.add_argument('--browser', default='chromium', choices=['chromium', 'firefox', 'webkit'])
    nav_parser.add_argument('--width', type=int, default=1280)
    nav_parser.add_argument('--height', type=int, default=720)
    nav_parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    nav_parser.add_argument('--timeout', type=int, default=30000)

    # Screenshot command
    shot_parser = subparsers.add_parser('screenshot', help='Take screenshot')
    shot_parser.add_argument('--name', required=True, help='Screenshot filename')
    shot_parser.add_argument('--selector', help='CSS selector for element screenshot')
    shot_parser.add_argument('--fullPage', action='store_true', help='Capture full page')
    shot_parser.add_argument('--savePng', action='store_true', default=True)

    # Console logs command
    console_parser = subparsers.add_parser('console', help='Get console logs')
    console_parser.add_argument('--type', default='all',
                               choices=['all', 'error', 'warning', 'log', 'info', 'debug'])
    console_parser.add_argument('--search', help='Search term')
    console_parser.add_argument('--limit', type=int, help='Max messages')
    console_parser.add_argument('--clear', action='store_true', help='Clear after reading')

    # Evaluate command
    eval_parser = subparsers.add_parser('evaluate', help='Execute JavaScript')
    eval_parser.add_argument('--script', required=True, help='JavaScript code')

    # Click command
    click_parser = subparsers.add_parser('click', help='Click element')
    click_parser.add_argument('--selector', required=True, help='CSS selector')

    # Fill command
    fill_parser = subparsers.add_parser('fill', help='Fill input field')
    fill_parser.add_argument('--selector', required=True, help='CSS selector')
    fill_parser.add_argument('--value', required=True, help='Value to fill')

    # Visible text command
    text_parser = subparsers.add_parser('visible-text', help='Get visible text')
    text_parser.add_argument('--selector', help='CSS selector')

    # Visible HTML command
    html_parser = subparsers.add_parser('visible-html', help='Get HTML')
    html_parser.add_argument('--selector', help='CSS selector')
    html_parser.add_argument('--cleanHtml', action='store_true')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        result = None

        if args.command == 'navigate':
            await session.start(
                browser_type=args.browser,
                headless=args.headless,
                width=args.width,
                height=args.height
            )
            result = await session.navigate(args.url, timeout=args.timeout)

        elif args.command == 'screenshot':
            result = await session.screenshot(
                name=args.name,
                selector=args.selector,
                full_page=args.fullPage,
                save_png=args.savePng
            )

        elif args.command == 'console':
            result = session.get_console_logs(
                log_type=args.type,
                search=args.search,
                limit=args.limit,
                clear=args.clear
            )

        elif args.command == 'evaluate':
            result = await session.evaluate(args.script)

        elif args.command == 'click':
            result = await session.click(args.selector)

        elif args.command == 'fill':
            result = await session.fill(args.selector, args.value)

        elif args.command == 'visible-text':
            result = await session.get_visible_text(args.selector)

        elif args.command == 'visible-html':
            result = await session.get_visible_html(
                selector=args.selector,
                clean_html=args.cleanHtml
            )

        # Print result as JSON
        if result is not None:
            if isinstance(result, (dict, list)):
                print(json.dumps(result, indent=2))
            else:
                print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Keep browser open for subsequent commands
        # await session.close()
        pass


if __name__ == '__main__':
    asyncio.run(main())
