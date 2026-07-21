"""
Pytest fixtures for Partner App QA framework.
Provides reusable fixtures for web, mobile, API, and database testing.
"""

import pytest
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Generator, Any, Dict
from faker import Faker
from core.playwright_manager import PlaywrightDriver
from core.appium_manager import AppiumDriverManager
from core.logger import logger
from core.screenshot_manager import ScreenshotManager
from pages.login.page import LoginPage
from pages.login.actions import LoginActions
from pages.login.assertions import LoginAssertions
from mobile_pages.login.actions import MobileLoginActions
from mobile_pages.login.assertions import MobileLoginAssertions
from mobile_pages.login.page import MobileLoginPage
from api.clients.auth_client import AuthAPIClient
from config.settings import settings


# ============================================================================
# Browser Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def browser_driver(request) -> Generator[PlaywrightDriver, None, None]:
    """
    Provide Playwright driver.
    
    Yields:
        PlaywrightDriver instance
    """
    driver = PlaywrightDriver()
    driver.initialize()
    logger.info("Browser driver initialized")
    
    yield driver
    
    video_path = driver.close()
    if video_path:
        logger.info(f"Playwright video saved: {video_path}")
        rep_call = getattr(request.node, "rep_call", None)
        if rep_call and rep_call.failed and settings.reporting.enable_allure:
            import allure

            allure.attach.file(
                str(video_path),
                name=f"{request.node.name} video",
                attachment_type=allure.attachment_type.MP4,
            )
    logger.info("Browser driver closed")


@pytest.fixture(scope="function")
def screenshot_manager() -> Generator[ScreenshotManager, None, None]:
    """
    Provide screenshot manager.
    
    Yields:
        ScreenshotManager instance
    """
    manager = ScreenshotManager()
    yield manager


# ============================================================================
# Mobile Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def mobile_driver(request) -> Generator[AppiumDriverManager, None, None]:
    """
    Provide Appium mobile driver and keep it open after the test.
    
    Yields:
        AppiumDriverManager instance
    """
    manager = AppiumDriverManager.get_instance()
    manager.initialize_driver()
    manager.start_screen_recording()
    logger.info("Mobile driver initialized")
    
    yield manager

    video_path = manager.stop_screen_recording(
        name=f"mobile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    )
    if video_path:
        logger.info(f"Mobile video saved: {video_path}")
        rep_call = getattr(request.node, "rep_call", None)
        if rep_call and rep_call.failed and settings.reporting.enable_allure:
            import allure

            allure.attach.file(
                str(video_path),
                name=f"{request.node.name} video",
                attachment_type=allure.attachment_type.MP4,
            )

    logger.info("Mobile driver kept open")


# ============================================================================
# Page Object Fixtures
# ============================================================================

@pytest.fixture(scope="function")
async def login_page_fixtures(browser_driver) -> Generator[tuple, None, None]:
    """
    Provide login page objects (page, actions, assertions).
    
    Yields:
        Tuple of (LoginPage, LoginActions, LoginAssertions)
    """
    page = browser_driver.get_page()
    
    login_page = LoginPage(page)
    login_actions = LoginActions(login_page)
    login_assertions = LoginAssertions(login_page)
    
    yield login_page, login_actions, login_assertions


@pytest.fixture(scope="function")
def mobile_login_page_fixtures(mobile_driver) -> Generator[tuple, None, None]:
    """Provide mobile login page, actions, and assertions for Appium BDD tests."""
    login_page = MobileLoginPage(mobile_driver.driver)
    login_actions = MobileLoginActions(login_page)
    login_assertions = MobileLoginAssertions(login_page)

    yield login_page, login_actions, login_assertions


# ============================================================================
# API Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def api_client() -> Generator[AuthAPIClient, None, None]:
    """
    Provide API client.
    
    Yields:
        AuthAPIClient instance
    """
    client = AuthAPIClient()
    yield client
    client.close()


@pytest.fixture(scope="function")
def authenticated_api_client(api_client) -> Generator[AuthAPIClient, None, None]:
    """
    Provide authenticated API client with valid token.
    
    Yields:
        AuthAPIClient instance with auth token
    """
    # Set a valid token (in real scenario, obtain from login)
    api_client.set_auth_token("dummy_token_for_testing")
    yield api_client


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def db() -> Generator[Any, None, None]:
    """
    Provide database manager (session scope).
    
    Yields:
        DatabaseManager instance
    """
    from database.db_manager import DatabaseManager

    database = DatabaseManager()
    database.initialize()
    
    yield database
    
    database.close()


@pytest.fixture(scope="function")
def db_transaction(db) -> Generator[Any, None, None]:
    """
    Provide transactional database session.
    Creates transaction that rolls back after test.
    
    Yields:
        Database session
    """
    session = db.get_session()
    
    yield session
    
    # Rollback to clean up test data
    session.rollback()
    session.close()


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def faker_instance() -> Generator[Faker, None, None]:
    """
    Provide Faker instance for generating test data.
    
    Yields:
        Faker instance
    """
    faker = Faker()
    yield faker


@pytest.fixture(scope="function")
def test_user_data(faker_instance) -> Dict[str, str]:
    """
    Generate test user data.
    
    Returns:
        Dictionary with user test data
    """
    return {
        "email": faker_instance.email(),
        "password": "TestPassword@123",
        "first_name": faker_instance.first_name(),
        "last_name": faker_instance.last_name(),
        "phone": faker_instance.phone_number(),
    }


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def test_env() -> str:
    """
    Get test environment.
    
    Returns:
        Environment name (dev, staging, prod)
    """
    return settings.environment


@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Get base URL for testing.
    
    Returns:
        Base URL
    """
    env = settings.environment
    
    urls = {
        "dev": "http://localhost:3000",
        "staging": "https://staging.partnerapp.com",
        "prod": "https://partnerapp.com",
    }
    
    return urls.get(env, urls["dev"])


# ============================================================================
# Cleanup Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def cleanup_screenshots():
    """
    Cleanup screenshots after test.
    
    Yields:
        Generator
    """
    yield
    
    try:
        manager = ScreenshotManager()
        old_screenshots = manager.cleanup_old_screenshots(days=0)
        logger.info(f"Cleaned up {old_screenshots} old screenshots")
    except Exception as e:
        logger.warning(f"Error cleaning up screenshots: {e}")


# ============================================================================
# Markers and Parametrization
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "sanity: mark test as sanity test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "critical: mark test as critical test")
    config.addinivalue_line("markers", "mobile: mark test as mobile test")
    config.addinivalue_line("markers", "android: mark test as android specific")
    config.addinivalue_line("markers", "ios: mark test as ios specific")
    config.addinivalue_line("markers", "ui: mark test as UI test")
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "db: mark test as database test")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")


# ============================================================================
# Hooks
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots on test failure and store report objects on the test item."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)

    if rep.when != "call" or not rep.failed:
        return

    if "browser_driver" in item.fixturenames:
        try:
            browser_driver = item.funcargs.get("browser_driver")
            if browser_driver:
                manager = ScreenshotManager()
                screenshot_path = manager.capture_screenshot(
                    browser_driver.get_page(),
                    name=f"failure_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    test_name=item.name,
                )
                logger.error(f"Test failed. Screenshot: {screenshot_path}")

                if settings.reporting.enable_allure and screenshot_path:
                    import allure

                    allure.attach.file(
                        str(screenshot_path),
                        name=f"{item.name} screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
        except Exception as e:
            logger.warning(f"Failed to capture browser failure evidence: {e}")

    if "mobile_driver" in item.fixturenames:
        try:
            mobile_driver = item.funcargs.get("mobile_driver")
            if mobile_driver and mobile_driver.driver:
                manager = ScreenshotManager()
                screenshot_path = manager.capture_screenshot(
                    mobile_driver.driver,
                    name=f"failure_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    test_name=item.name,
                )
                logger.error(f"Mobile test failed. Screenshot: {screenshot_path}")

                if settings.reporting.enable_allure and screenshot_path:
                    import allure

                    allure.attach.file(
                        str(screenshot_path),
                        name=f"{item.name} screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
        except Exception as e:
            logger.warning(f"Failed to capture mobile failure evidence: {e}")
