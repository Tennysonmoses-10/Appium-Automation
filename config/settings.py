"""
Configuration management for Partner App QA automation framework.
Supports environment-based configuration with Pydantic validation.
"""

from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    username: str = Field(default="postgres")
    password: str = Field(default="")
    database: str = Field(default="partner_app")
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=20)
    echo: bool = Field(default=False)


class AppiumConfig(BaseSettings):
    """Appium configuration for mobile automation."""
    
    server_url: str = Field(default="http://localhost:4723")
    timeout: int = Field(default=30)
    implicit_wait: int = Field(default=10)
    explicit_wait: int = Field(default=20)
    device_name: str = Field(default="emulator-5554")
    platform: Literal["Android", "iOS"] = Field(default="Android")
    app_package: str = Field(default="com.partnerapp")
    app_activity: str = Field(default=".MainActivity")


class PlaywrightConfig(BaseSettings):
    """Playwright configuration for web automation."""
    
    browser_type: Literal["chromium", "firefox", "webkit"] = Field(default="chromium")
    headless: bool = Field(default=True)
    slow_mo: int = Field(default=0)
    timeout: int = Field(default=30000)
    viewport_width: int = Field(default=1920)
    viewport_height: int = Field(default=1080)
    record_video: bool = Field(default=False)
    record_trace: bool = Field(default=False)


class ReportingConfig(BaseSettings):
    """Reporting configuration."""
    
    allure_dir: Path = Field(default=Path("reports/allure"))
    html_dir: Path = Field(default=Path("reports/html"))
    screenshot_dir: Path = Field(default=Path("screenshots"))
    video_dir: Path = Field(default=Path("videos"))
    logs_dir: Path = Field(default=Path("logs"))
    enable_allure: bool = Field(default=True)
    enable_html: bool = Field(default=True)
    slack_enabled: bool = Field(default=False)
    slack_webhook: str = Field(default="")
    email_enabled: bool = Field(default=False)
    email_recipients: list[str] = Field(default_factory=list)


class APIConfig(BaseSettings):
    """API configuration."""
    
    base_url: str = Field(default="http://localhost:8080")
    timeout: int = Field(default=30)
    retry_count: int = Field(default=3)
    retry_delay: int = Field(default=1)
    verify_ssl: bool = Field(default=True)


class AppSettings(BaseSettings):
    """Main application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # Environment
    environment: Literal["dev", "staging", "prod"] = Field(default="dev")
    
    # Application
    app_name: str = Field(default="partner-app-qa")
    app_version: str = Field(default="1.0.0")
    
    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO")
    log_format: str = Field(default="json")
    enable_console_logging: bool = Field(default=True)
    
    # Execution
    parallel_workers: int = Field(default=4)
    test_timeout: int = Field(default=300)
    headless_mode: bool = Field(default=True)
    
    # Sub-configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    appium: AppiumConfig = Field(default_factory=AppiumConfig)
    playwright: PlaywrightConfig = Field(default_factory=PlaywrightConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    
    # Retry configuration
    max_retries: int = Field(default=3)
    retry_delay_seconds: int = Field(default=2)
    
    # Screenshot configuration
    capture_screenshot_on_failure: bool = Field(default=True)
    capture_video_on_failure: bool = Field(default=True)
    
    # Test data
    test_data_dir: Path = Field(default=Path("test_data"))
    
    def get_database_url(self) -> str:
        """Generate database URL from configuration."""
        return (
            f"postgresql://{self.database.username}:{self.database.password}"
            f"@{self.database.host}:{self.database.port}/{self.database.database}"
        )
    
    def get_api_base_url(self) -> str:
        """Get API base URL."""
        return self.api.base_url


# Global settings instance
settings = AppSettings()
