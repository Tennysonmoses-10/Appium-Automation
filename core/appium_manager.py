"""
Appium driver manager for mobile automation.
Handles iOS and Android device management and lifecycle.
"""

import base64
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from config.settings import settings
from core.logger import logger


class AppiumDriverManager:
    """Manage Appium drivers for mobile automation."""
    
    _instances: Dict[str, "AppiumDriverManager"] = {}
    
    def __init__(self, device_id: str = "default"):
        """
        Initialize AppiumDriverManager.
        
        Args:
            device_id: Unique identifier for device
        """
        self.device_id = device_id
        self.driver = None
        self._screenshot_dir = settings.reporting.screenshot_dir
        self._video_dir = settings.reporting.video_dir
        self._screen_recording = False
    
    @classmethod
    def get_instance(cls, device_id: str = "default") -> "AppiumDriverManager":
        """
        Get or create singleton instance for device.
        
        Args:
            device_id: Device identifier
            
        Returns:
            AppiumDriverManager instance
        """
        if device_id not in cls._instances:
            cls._instances[device_id] = cls(device_id)
        return cls._instances[device_id]
    
    def initialize_android_driver(self) -> Any:
        """
        Initialize Android driver using UiAutomator2.
        
        Returns:
            WebDriver instance
        """
        try:
            options = UiAutomator2Options()
            options.device_name = settings.appium.device_name
            options.platform_name = "Android"
            options.app_package = settings.appium.app_package
            options.app_activity = settings.appium.app_activity
            options.automation_name = settings.appium.automation_name
            options.implicit_wait_timeout = settings.appium.implicit_wait * 1000
            options.new_command_timeout = settings.appium.timeout * 1000
            if settings.appium.app_path:
                options.app = settings.appium.app_path
            if settings.appium.udid:
                options.udid = settings.appium.udid
            
            # Optional: Set more capabilities
            options.set_capability("autoGrantPermissions", True)
            options.set_capability("noReset", True)
            options.set_capability("allowInsecureLocalhost", True)
            
            self.driver = webdriver.Remote(
                settings.appium.server_url,
                options=options
            )
            
            logger.info(
                f"Android driver initialized for device: {settings.appium.device_name}"
            )
            return self.driver
        
        except Exception as e:
            logger.error(f"Failed to initialize Android driver: {e}")
            raise
    
    def initialize_ios_driver(self) -> Any:
        """
        Initialize iOS driver using XCUITest.
        
        Returns:
            WebDriver instance
        """
        try:
            options = XCUITestOptions()
            options.device_name = settings.appium.device_name
            options.platform_name = "iOS"
            options.bundle_id = settings.appium.app_package
            options.automation_name = settings.appium.automation_name
            options.implicit_wait_timeout = settings.appium.implicit_wait * 1000
            options.new_command_timeout = settings.appium.timeout * 1000
            if settings.appium.app_path:
                options.app = settings.appium.app_path
            if settings.appium.udid:
                options.udid = settings.appium.udid
            
            # Optional: Set more capabilities
            options.set_capability("autoAcceptAlerts", True)
            options.set_capability("allowInsecureLocalhost", True)
            
            self.driver = webdriver.Remote(
                settings.appium.server_url,
                options=options
            )
            
            logger.info(
                f"iOS driver initialized for device: {settings.appium.device_name}"
            )
            return self.driver
        
        except Exception as e:
            logger.error(f"Failed to initialize iOS driver: {e}")
            raise
    
    def initialize_driver(self) -> Any:
        """
        Initialize driver based on platform setting.
        
        Returns:
            WebDriver instance
        """
        if self.driver:
            logger.info(f"Reusing existing Appium driver for device: {self.device_id}")
            return self.driver

        if settings.appium.platform == "Android":
            return self.initialize_android_driver()
        elif settings.appium.platform == "iOS":
            return self.initialize_ios_driver()
        else:
            raise ValueError(f"Unsupported platform: {settings.appium.platform}")
    
    def close_driver(self) -> None:
        """Close driver and cleanup resources."""
        try:
            if self.driver:
                self.driver.quit()
                logger.info(f"Driver closed for device: {self.device_id}")
        except Exception as e:
            logger.error(f"Error closing driver: {e}")
    
    def start_screen_recording(self) -> bool:
        """Start Appium screen recording when enabled for the current platform."""
        if not self.driver or self._screen_recording:
            return False

        if not (settings.appium.record_video or settings.capture_video_each_scenario):
            return False

        try:
            self.driver.start_recording_screen()
            self._screen_recording = True
            logger.info("Mobile screen recording started")
            return True
        except Exception as e:
            logger.warning(f"Mobile screen recording is not available: {e}")
            return False

    def stop_screen_recording(self, name: str = None) -> Optional[Path]:
        """Stop Appium screen recording and save the video file."""
        if not self.driver or not self._screen_recording:
            return None

        try:
            payload = self.driver.stop_recording_screen()
            self._screen_recording = False
            if not payload:
                return None

            self._video_dir.mkdir(parents=True, exist_ok=True)
            if not name:
                name = f"mobile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

            video_path = self._video_dir / name
            video_path.write_bytes(base64.b64decode(payload))
            logger.info(f"Mobile screen recording saved: {video_path}")
            return video_path
        except Exception as e:
            self._screen_recording = False
            logger.warning(f"Failed to stop mobile screen recording: {e}")
            return None

    def take_screenshot(self, name: str = None) -> Path:
        """
        Take screenshot of mobile screen.
        
        Args:
            name: Screenshot filename (optional)
            
        Returns:
            Path to screenshot file
        """
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        
        try:
            self._screenshot_dir.mkdir(parents=True, exist_ok=True)
            
            if not name:
                name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            screenshot_path = self._screenshot_dir / name
            self.driver.save_screenshot(str(screenshot_path))
            
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    def rotate_device(self, orientation: str) -> None:
        """
        Rotate device to specified orientation.
        
        Args:
            orientation: "PORTRAIT" or "LANDSCAPE"
        """
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        
        try:
            self.driver.orientation = orientation
            logger.info(f"Device rotated to: {orientation}")
        except Exception as e:
            logger.error(f"Failed to rotate device: {e}")
    
    def get_device_info(self) -> Dict[str, Any]:
        """
        Get device information.
        
        Returns:
            Dictionary with device info
        """
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        
        try:
            return {
                "device_name": self.driver.capabilities.get("deviceName"),
                "platform": self.driver.capabilities.get("platformName"),
                "os_version": self.driver.capabilities.get("platformVersion"),
                "app_package": self.driver.capabilities.get("appPackage"),
                "orientation": self.driver.orientation,
            }
        except Exception as e:
            logger.error(f"Failed to get device info: {e}")
            raise
    
    def install_app(self, app_path: str) -> None:
        """
        Install application on device.
        
        Args:
            app_path: Path to application file
        """
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        
        try:
            self.driver.install_app(app_path)
            logger.info(f"App installed: {app_path}")
        except Exception as e:
            logger.error(f"Failed to install app: {e}")
            raise
    
    def uninstall_app(self, app_package: str) -> None:
        """
        Uninstall application from device.
        
        Args:
            app_package: Package name or bundle ID
        """
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        
        try:
            self.driver.remove_app(app_package)
            logger.info(f"App uninstalled: {app_package}")
        except Exception as e:
            logger.error(f"Failed to uninstall app: {e}")
            raise
