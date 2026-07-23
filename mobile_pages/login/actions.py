"""Business workflows for the mobile login screen."""

from core.logger import logger
from mobile_pages.login.page import MobileLoginPage


class MobileLoginActions:
    """Composes login-screen interactions into reusable user flows."""

    def __init__(self, page: MobileLoginPage):
        self.page = page

    def proceed_button(self) -> None:
        self.page.proceed_button()
        logger.info("Submitted mobile proceed action")

    def get_started(self) -> None:
        self.page.get_started()
        logger.info("Submitted mobile get started action")

    def enter_mobile_number(self, mobile_number: str) -> None:
        self.page.enter_mobilenumbers(mobile_number)
        logger.info("Submitted mobile number entry action")

    def proceed_login(self) -> None:
        self.page.Proceed_Login()
        logger.info("Submitted mobile proceed login action")

    def enter_otp(self, otp: str) -> None:
        self.page.enter_otp(otp)
        logger.info("Submitted OTP entry action")

    def confirm_otp(self) -> None:
        self.page.confirm_otp()
        logger.info("Submitted OTP confirm action")

    def click_advisory(self) -> None:
        self.page.click_advisory()
        logger.info("Clicked mobile advisory action")

    def advisory_button(self) -> None:
        """Backward-compatible alias for the advisory action."""
        self.click_advisory()

    def click_ask_expert(self) -> None:
        self.page.click_ask_expert()
        logger.info("Clicked mobile Ask Expert action")

    def ask_expert_button(self) -> None:
        """Backward-compatible alias for the Ask Expert action."""
        self.click_ask_expert()

    def login(self, email: str, password: str) -> None:
        self.page.enter_email(email)
        self.page.enter_password(password)
        self.page.click_login()
        logger.info("Submitted mobile login credentials")
