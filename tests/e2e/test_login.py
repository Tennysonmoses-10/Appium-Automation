"""
Example test: Login functionality using Page Object Model.
Demonstrates integration of all framework components.
"""

import pytest
from core.logger import logger
from pages.login.page import LoginPage
from pages.login.actions import LoginActions
from pages.login.assertions import LoginAssertions


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.critical
@pytest.mark.ui
class TestLoginUI:
    """Login page UI tests."""
    
    @pytest.fixture(autouse=True)
    async def setup(self, browser_driver, base_url):
        """Setup test."""
        self.browser_driver = browser_driver
        self.page = browser_driver.get_page()
        self.base_url = base_url
        
        # Navigate to login page
        await self.page.goto(f"{self.base_url}/login", wait_until="networkidle")
    
    async def test_login_page_loaded(self):
        """Test: Login page loads successfully."""
        logger.info("Testing login page load...")
        
        # Check page title
        page_title = await self.page.title()
        assert "Login" in page_title
        
        # Check key elements are visible
        email_input = await self.page.locator("//input[@id='email']").is_visible()
        password_input = await self.page.locator("//input[@id='password']").is_visible()
        login_button = await self.page.locator("//button[@id='login-btn']").is_visible()
        
        assert email_input, "Email input not visible"
        assert password_input, "Password input not visible"
        assert login_button, "Login button not visible"
        
        logger.info("✓ Login page loaded successfully")
    
    async def test_valid_login(self, test_user_data):
        """Test: Successful login with valid credentials."""
        logger.info("Testing valid login...")
        
        login_page = LoginPage(self.page)
        actions = LoginActions(login_page)
        assertions = LoginAssertions(login_page)
        
        # Verify page loaded
        assert await assertions.verify_page_loaded()
        
        # Perform login
        await actions.perform_login(
            test_user_data["email"],
            test_user_data["password"],
            remember_me=False
        )
        
        # Verify success
        assert await assertions.verify_success_message()
        
        logger.info("✓ Valid login test passed")
    
    async def test_invalid_email_format(self):
        """Test: Login with invalid email format."""
        logger.info("Testing invalid email format...")
        
        login_page = LoginPage(self.page)
        assertions = LoginAssertions(login_page)
        
        await login_page.enter_email("invalid-email")
        await login_page.enter_password("TestPassword@123")
        await login_page.click_login_button()
        
        # Verify error
        assert await assertions.verify_email_error()
        
        logger.info("✓ Invalid email format test passed")
    
    async def test_empty_credentials(self):
        """Test: Login with empty credentials."""
        logger.info("Testing empty credentials...")
        
        login_page = LoginPage(self.page)
        actions = LoginActions(login_page)
        
        await actions.perform_login_with_empty_fields()
        
        # Verify validation errors appear
        email_visible = await login_page.page.locator(
            "//span[@id='email-error']"
        ).is_visible()
        
        assert email_visible, "Validation error should appear"
        
        logger.info("✓ Empty credentials test passed")
    
    async def test_remember_me_functionality(self, test_user_data):
        """Test: Remember me checkbox works."""
        logger.info("Testing remember me functionality...")
        
        login_page = LoginPage(self.page)
        actions = LoginActions(login_page)
        assertions = LoginAssertions(login_page)
        
        await login_page.enter_email(test_user_data["email"])
        await login_page.enter_password(test_user_data["password"])
        await login_page.check_remember_me()
        
        # Verify checkbox is checked
        assert await assertions.verify_remember_me_state(True)
        
        logger.info("✓ Remember me functionality test passed")


@pytest.mark.regression
@pytest.mark.api
class TestLoginAPI:
    """Login API tests."""
    
    async def test_login_api_success(self, api_client, test_user_data):
        """Test: Login API returns successful response."""
        logger.info("Testing login API...")
        
        try:
            response = await api_client.login(
                test_user_data["email"],
                test_user_data["password"]
            )
            
            assert response is not None
            assert "access_token" in response or "token" in response
            
            logger.info("✓ Login API test passed")
        
        except Exception as e:
            logger.error(f"Login API test failed: {e}")
            raise
    
    async def test_login_api_invalid_credentials(self, api_client):
        """Test: Login API rejects invalid credentials."""
        logger.info("Testing login API with invalid credentials...")
        
        with pytest.raises(Exception):
            await api_client.login("invalid@test.com", "invalid_password")
        
        logger.info("✓ Invalid credentials rejection test passed")


@pytest.mark.db
@pytest.mark.regression
class TestLoginDatabase:
    """Login database validation tests."""
    
    def test_user_exists_in_database(self, db, test_user_data):
        """Test: Verify user exists in database."""
        logger.info("Testing database user lookup...")
        
        user = db.get_user_by_email(test_user_data["email"])
        
        assert user is not None
        assert user["email"] == test_user_data["email"]
        
        logger.info("✓ Database user lookup test passed")
    
    def test_user_created_with_correct_status(self, db):
        """Test: New user created with correct status."""
        logger.info("Testing user creation in database...")
        
        email = "newuser@test.com"
        password_hash = "hashed_password_here"
        
        user = db.create_user(
            email=email,
            password_hash=password_hash,
            name="Test User"
        )
        
        assert user is not None
        assert user["email"] == email
        assert user["name"] == "Test User"
        
        # Cleanup
        if user:
            db.delete_user(user["id"])
        
        logger.info("✓ User creation test passed")


# ============================================================================
# Parametrized Tests
# ============================================================================

@pytest.mark.parametrize("email,password,should_succeed", [
    ("valid@test.com", "ValidPass@123", True),
    ("invalid@test.com", "InvalidPass@123", False),
    ("", "Password@123", False),
    ("test@example.com", "", False),
])
async def test_login_parametrized(
    browser_driver,
    base_url,
    email,
    password,
    should_succeed
):
    """Parametrized login test with multiple scenarios."""
    logger.info(f"Testing login with email={email}, should_succeed={should_succeed}")
    
    page = browser_driver.get_page()
    await page.goto(f"{base_url}/login", wait_until="networkidle")
    
    login_page = LoginPage(page)
    await login_page.enter_email(email)
    await login_page.enter_password(password)
    await login_page.click_login_button()
    
    assertions = LoginAssertions(login_page)
    
    if should_succeed:
        assert await assertions.verify_success_message()
    else:
        assert await assertions.verify_error_message()
    
    logger.info(f"✓ Parametrized login test passed")
