"""
Wait utilities for explicit waits with retry mechanisms.
Implements WebDriverWait patterns with custom conditions.
"""

from typing import TypeVar, Callable, Any, Optional
from datetime import datetime, timedelta
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)
from core.logger import logger

T = TypeVar("T")


class ExplicitWait:
    """Explicit wait handler with configurable timeout and polling."""
    
    def __init__(
        self,
        timeout: int = 10,
        poll_frequency: float = 0.5,
    ):
        """
        Initialize ExplicitWait.
        
        Args:
            timeout: Maximum wait time in seconds
            poll_frequency: How often to check condition in seconds
        """
        self.timeout = timeout
        self.poll_frequency = poll_frequency
    
    def wait_for(
        self,
        condition: Callable[[], bool],
        message: str = "Condition not met",
    ) -> bool:
        """
        Wait for a condition to be true.
        
        Args:
            condition: Callable that returns True when condition is met
            message: Message to log if timeout occurs
            
        Returns:
            True if condition met, False if timeout
        """
        end_time = datetime.now() + timedelta(seconds=self.timeout)
        
        while datetime.now() < end_time:
            try:
                if condition():
                    return True
            except Exception as e:
                logger.debug(f"Condition check failed: {e}")
            
            time.sleep(self.poll_frequency)
        
        logger.warning(f"Wait timeout after {self.timeout}s: {message}")
        return False
    
    def wait_for_value(
        self,
        getter: Callable[[], Any],
        expected_value: Any,
        message: str = "Value not matched",
    ) -> bool:
        """
        Wait for a value to match expected value.
        
        Args:
            getter: Callable that returns the current value
            expected_value: Expected value to match
            message: Message to log if timeout occurs
            
        Returns:
            True if value matched, False if timeout
        """
        return self.wait_for(
            lambda: getter() == expected_value,
            message
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception),
    )
    def wait_for_with_retry(
        self,
        operation: Callable[[], T],
        message: str = "Operation failed after retries",
    ) -> T:
        """
        Execute operation with automatic retry on failure.
        
        Args:
            operation: Callable to execute
            message: Message to log if all retries fail
            
        Returns:
            Result of operation
            
        Raises:
            RetryError: If operation fails after all retries
        """
        try:
            return operation()
        except Exception as e:
            logger.error(f"Operation failed: {e}. Retrying...")
            raise


class WaitCondition:
    """Predefined wait conditions for common scenarios."""
    
    @staticmethod
    def element_visible(
        get_element: Callable[[], Any],
        timeout: int = 10,
    ) -> bool:
        """Wait for element to be visible."""
        waiter = ExplicitWait(timeout=timeout)
        return waiter.wait_for(
            lambda: hasattr(get_element(), "is_visible") and get_element().is_visible(),
            "Element not visible"
        )
    
    @staticmethod
    def element_enabled(
        get_element: Callable[[], Any],
        timeout: int = 10,
    ) -> bool:
        """Wait for element to be enabled."""
        waiter = ExplicitWait(timeout=timeout)
        return waiter.wait_for(
            lambda: hasattr(get_element(), "is_enabled") and get_element().is_enabled(),
            "Element not enabled"
        )
    
    @staticmethod
    def element_hidden(
        get_element: Callable[[], Any],
        timeout: int = 10,
    ) -> bool:
        """Wait for element to be hidden."""
        waiter = ExplicitWait(timeout=timeout)
        return waiter.wait_for(
            lambda: not hasattr(get_element(), "is_visible") or not get_element().is_visible(),
            "Element still visible"
        )
    
    @staticmethod
    def text_present(
        get_text: Callable[[], str],
        expected_text: str,
        timeout: int = 10,
    ) -> bool:
        """Wait for expected text to be present."""
        waiter = ExplicitWait(timeout=timeout)
        return waiter.wait_for(
            lambda: expected_text in get_text(),
            f"Text '{expected_text}' not found"
        )
    
    @staticmethod
    def url_contains(
        get_url: Callable[[], str],
        expected_url_part: str,
        timeout: int = 10,
    ) -> bool:
        """Wait for URL to contain expected part."""
        waiter = ExplicitWait(timeout=timeout)
        return waiter.wait_for(
            lambda: expected_url_part in get_url(),
            f"URL does not contain '{expected_url_part}'"
        )
