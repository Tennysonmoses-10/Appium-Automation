"""Business workflows for the mobile login screen."""

from core.logger import logger
from mobile_pages.login.page import MobileLoginPage


class MobileLoginActions:
    """Composes login-screen interactions into reusable user flows."""

    def __init__(self, page: MobileLoginPage):
        self.page = page

    def login(self, email: str, password: str) -> None:
        self.page.enter_email(email)
        self.page.enter_password(password)
        self.page.click_login()
        logger.info("Submitted mobile login credentials")
