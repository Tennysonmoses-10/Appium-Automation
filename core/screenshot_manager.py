"""
Screenshot and evidence capture manager.
Automatically captures screenshots on failures and manages evidence storage.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Any
from functools import wraps
from core.logger import logger
from config.settings import settings


class ScreenshotManager:
    """Manage screenshot capture and storage."""
    
    def __init__(self):
        """Initialize ScreenshotManager."""
        self.screenshot_dir = settings.reporting.screenshot_dir
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    def capture_screenshot(
        self,
        driver: Any,
        name: str = None,
        test_name: str = None,
    ) -> Path:
        """
        Capture screenshot from driver.
        
        Args:
            driver: WebDriver or mobile driver instance
            name: Optional screenshot name
            test_name: Optional test name for context
            
        Returns:
            Path to screenshot file
        """
        try:
            if not name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                name = f"screenshot_{timestamp}.png"
            
            screenshot_path = self.screenshot_dir / name
            
            # Handle both sync and async drivers
            if hasattr(driver, "save_screenshot"):
                # Mobile driver
                driver.save_screenshot(str(screenshot_path))
            elif hasattr(driver, "screenshot"):
                # Playwright or similar
                driver.screenshot(path=str(screenshot_path))
            else:
                logger.warning(f"Driver type not recognized for screenshot: {type(driver)}")
                return None
            
            logger.info(f"Screenshot captured: {screenshot_path}")
            
            if test_name:
                logger.info(f"Screenshot for test: {test_name}")
            
            return screenshot_path
        
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None
    
    def capture_on_failure(self, driver: Any, test_name: str):
        """
        Decorator to capture screenshot on test failure.
        
        Args:
            driver: WebDriver instance
            test_name: Name of test
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    screenshot_path = self.capture_screenshot(
                        driver,
                        name=f"failure_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        test_name=test_name
                    )
                    logger.error(
                        f"Test failed: {test_name}. Screenshot: {screenshot_path}. Error: {e}"
                    )
                    raise
            return wrapper
        return decorator
    
    def capture_page_source(self, driver: Any, test_name: str) -> Optional[Path]:
        """
        Capture page source HTML.
        
        Args:
            driver: WebDriver instance
            test_name: Name of test
            
        Returns:
            Path to HTML file
        """
        try:
            html_dir = settings.reporting.logs_dir / "page_sources"
            html_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_file = html_dir / f"source_{test_name}_{timestamp}.html"
            
            if hasattr(driver, "page_source"):
                page_source = driver.page_source
            elif hasattr(driver, "content"):
                page_source = driver.content
            else:
                logger.warning("Cannot capture page source from driver")
                return None
            
            html_file.write_text(page_source, encoding="utf-8")
            logger.info(f"Page source saved: {html_file}")
            
            return html_file
        
        except Exception as e:
            logger.error(f"Failed to capture page source: {e}")
            return None
    
    def get_screenshot_count(self) -> int:
        """
        Get total screenshot count in directory.
        
        Returns:
            Number of screenshots
        """
        return len(list(self.screenshot_dir.glob("*.png")))
    
    def cleanup_old_screenshots(self, days: int = 7) -> int:
        """
        Remove screenshots older than specified days.
        
        Args:
            days: Number of days to retain
            
        Returns:
            Number of files deleted
        """
        try:
            from datetime import timedelta
            import time
            
            cutoff_time = time.time() - (days * 86400)
            deleted_count = 0
            
            for screenshot_file in self.screenshot_dir.glob("*.png"):
                if screenshot_file.stat().st_mtime < cutoff_time:
                    screenshot_file.unlink()
                    deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old screenshots")
            return deleted_count
        
        except Exception as e:
            logger.error(f"Failed to cleanup screenshots: {e}")
            return 0


class VideoRecorder:
    """Manage video recording of test execution."""
    
    def __init__(self):
        """Initialize VideoRecorder."""
        self.video_dir = settings.reporting.video_dir
        self.video_dir.mkdir(parents=True, exist_ok=True)
    
    def get_video_path(self, test_name: str) -> Path:
        """
        Get video file path for test.
        
        Args:
            test_name: Name of test
            
        Returns:
            Path to video file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.video_dir / f"video_{test_name}_{timestamp}.mp4"
    
    def is_video_recording_enabled(self) -> bool:
        """Check if video recording is enabled."""
        return settings.playwright.record_video or getattr(
            settings, "mobile_video_recording", False
        )
    
    def cleanup_old_videos(self, days: int = 7) -> int:
        """
        Remove videos older than specified days.
        
        Args:
            days: Number of days to retain
            
        Returns:
            Number of files deleted
        """
        try:
            import time
            
            cutoff_time = time.time() - (days * 86400)
            deleted_count = 0
            
            for video_file in self.video_dir.glob("*.mp4"):
                if video_file.stat().st_mtime < cutoff_time:
                    video_file.unlink()
                    deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old videos")
            return deleted_count
        
        except Exception as e:
            logger.error(f"Failed to cleanup videos: {e}")
            return 0
