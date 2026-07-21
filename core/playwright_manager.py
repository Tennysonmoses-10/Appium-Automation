"""
Playwright driver manager for web UI automation.
Handles browser instantiation, lifecycle, and resource cleanup.
"""

from typing import Optional
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config.settings import settings
from core.logger import logger
import asyncio


class PlaywrightDriverManager:
    """Manage Playwright browser instances with context management."""
    
    _instance: Optional["PlaywrightDriverManager"] = None
    
    def __init__(self):
        """Initialize PlaywrightDriverManager."""
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._recording_dir = settings.reporting.video_dir
        self._trace_dir = settings.reporting.logs_dir / "traces"
        self.last_video_path: Optional[Path] = None
    
    @classmethod
    def get_instance(cls) -> "PlaywrightDriverManager":
        """Get singleton instance of PlaywrightDriverManager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    async def initialize_browser(self) -> Page:
        """
        Initialize browser with configuration.
        
        Returns:
            Page instance ready for automation
        """
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser based on configuration
            launch_options = {
                "headless": settings.playwright.headless,
                "slow_mo": settings.playwright.slow_mo,
            }
            
            if settings.playwright.browser_type == "chromium":
                self.browser = await self.playwright.chromium.launch(**launch_options)
            elif settings.playwright.browser_type == "firefox":
                self.browser = await self.playwright.firefox.launch(**launch_options)
            elif settings.playwright.browser_type == "webkit":
                self.browser = await self.playwright.webkit.launch(**launch_options)
            else:
                raise ValueError(f"Unsupported browser: {settings.playwright.browser_type}")
            
            # Create context with optional recording
            context_options = {
                "viewport": {
                    "width": settings.playwright.viewport_width,
                    "height": settings.playwright.viewport_height,
                },
            }
            
            if settings.playwright.record_video or settings.capture_video_each_scenario:
                self._recording_dir.mkdir(parents=True, exist_ok=True)
                context_options["record_video_dir"] = str(self._recording_dir)
            
            if settings.playwright.record_trace:
                self._trace_dir.mkdir(parents=True, exist_ok=True)
                context_options["record_trace_dir"] = str(self._trace_dir)
            
            self.context = await self.browser.new_context(**context_options)
            self.page = await self.context.new_page()
            
            # Set timeout
            self.page.set_default_timeout(settings.playwright.timeout)
            
            logger.info(
                f"Browser initialized: {settings.playwright.browser_type}, "
                f"headless={settings.playwright.headless}"
            )
            
            return self.page
        
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise
    
    async def close_browser(self) -> Optional[Path]:
        """Close browser and cleanup resources."""
        self.last_video_path = None
        try:
            if self.page and self.page.video:
                try:
                    self.last_video_path = Path(await self.page.video.path())
                except Exception as e:
                    logger.warning(f"Unable to resolve Playwright video path: {e}")

            if self.page:
                await self.page.close()
                logger.info("Page closed")
            
            if self.context:
                await self.context.close()
                logger.info("Context closed")
            
            if self.browser:
                await self.browser.close()
                logger.info("Browser closed")
            
            if self.playwright:
                await self.playwright.stop()
                logger.info("Playwright stopped")

            if self.last_video_path and self.last_video_path.exists():
                logger.info(f"Playwright video saved: {self.last_video_path}")
                return self.last_video_path
        
        except Exception as e:
            logger.error(f"Error closing browser: {e}")

        return self.last_video_path
    
    async def navigate(self, url: str) -> None:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
        """
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        try:
            await self.page.goto(url, wait_until="networkidle")
            logger.info(f"Navigated to: {url}")
        except Exception as e:
            logger.error(f"Navigation failed to {url}: {e}")
            raise
    
    async def take_screenshot(self, name: str = None) -> Path:
        """
        Take screenshot of current page.
        
        Args:
            name: Screenshot filename (optional)
            
        Returns:
            Path to screenshot file
        """
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        try:
            screenshots_dir = settings.reporting.screenshot_dir
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            if not name:
                name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            screenshot_path = screenshots_dir / name
            await self.page.screenshot(path=str(screenshot_path))
            
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    async def get_page_source(self) -> str:
        """
        Get page source HTML.
        
        Returns:
            Page HTML content
        """
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        return await self.page.content()
    
    async def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current URL
        """
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        return self.page.url


# Synchronous wrapper for pytest integration
class PlaywrightDriver:
    """Synchronous wrapper around async Playwright driver."""
    
    def __init__(self):
        """Initialize driver."""
        self.manager = PlaywrightDriverManager.get_instance()
        self._loop = None
    
    def _get_loop(self) -> asyncio.AbstractEventLoop:
        """Get or create event loop."""
        try:
            self._loop = asyncio.get_event_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop
    
    def initialize(self) -> Page:
        """Initialize browser."""
        loop = self._get_loop()
        return loop.run_until_complete(self.manager.initialize_browser())
    
    def close(self) -> Optional[Path]:
        """Close browser."""
        loop = self._get_loop()
        return loop.run_until_complete(self.manager.close_browser())
    
    def get_page(self) -> Page:
        """Get current page."""
        return self.manager.page
    
    def navigate(self, url: str) -> None:
        """Navigate to URL."""
        loop = self._get_loop()
        loop.run_until_complete(self.manager.navigate(url))
    
    def take_screenshot(self, name: str = None) -> Path:
        """Take screenshot."""
        loop = self._get_loop()
        return loop.run_until_complete(self.manager.take_screenshot(name))
