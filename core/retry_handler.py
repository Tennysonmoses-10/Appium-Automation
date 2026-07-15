"""
Retry handler with exponential backoff and circuit breaker pattern.
Provides resilient retry mechanisms for flaky operations.
"""

from typing import TypeVar, Callable, Any, Optional, Type
from functools import wraps
from datetime import datetime, timedelta
from enum import Enum
import time
from core.logger import logger

T = TypeVar("T")


class RetryStrategy(Enum):
    """Retry strategy options."""
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIBONACCI = "fibonacci"
    FIXED = "fixed"


class RetryException(Exception):
    """Raised when all retry attempts are exhausted."""
    pass


class CircuitBreakerException(Exception):
    """Raised when circuit breaker is open."""
    pass


class CircuitBreaker:
    """
    Circuit breaker pattern implementation.
    Prevents repeated attempts to execute failing operations.
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        name: str = "default",
    ):
        """
        Initialize CircuitBreaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Timeout in seconds before attempting recovery
            name: Name of circuit breaker
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, operation: Callable[[], T]) -> T:
        """
        Execute operation with circuit breaker protection.
        
        Args:
            operation: Callable to execute
            
        Returns:
            Result of operation
            
        Raises:
            CircuitBreakerException: If circuit is open
        """
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
                logger.info(f"Circuit breaker '{self.name}' entering half-open state")
            else:
                raise CircuitBreakerException(
                    f"Circuit breaker '{self.name}' is open"
                )
        
        try:
            result = operation()
            self._on_success()
            return result
        
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self) -> None:
        """Handle successful operation."""
        if self.state == "half-open":
            logger.info(f"Circuit breaker '{self.name}' closing")
            self.state = "closed"
        
        self.failure_count = 0
    
    def _on_failure(self) -> None:
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            logger.warning(
                f"Circuit breaker '{self.name}' opening after {self.failure_count} failures"
            )
            self.state = "open"
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt reset."""
        if not self.last_failure_time:
            return True
        
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.recovery_timeout


class RetryHandler:
    """Handle retry logic with multiple strategies."""
    
    _circuit_breakers: dict[str, CircuitBreaker] = {}
    
    @staticmethod
    def retry(
        max_attempts: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_multiplier: float = 2.0,
        exceptions: tuple[Type[Exception], ...] = (Exception,),
        circuit_breaker_name: Optional[str] = None,
    ):
        """
        Decorator for retry logic.
        
        Args:
            max_attempts: Maximum retry attempts
            strategy: Retry strategy (exponential, linear, fibonacci, fixed)
            base_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            backoff_multiplier: Multiplier for exponential backoff
            exceptions: Tuple of exceptions to catch and retry
            circuit_breaker_name: Optional circuit breaker name
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> T:
                attempt = 0
                last_exception = None
                
                # Get or create circuit breaker
                circuit_breaker = None
                if circuit_breaker_name:
                    if circuit_breaker_name not in RetryHandler._circuit_breakers:
                        RetryHandler._circuit_breakers[circuit_breaker_name] = CircuitBreaker(
                            name=circuit_breaker_name
                        )
                    circuit_breaker = RetryHandler._circuit_breakers[circuit_breaker_name]
                
                while attempt < max_attempts:
                    try:
                        if circuit_breaker:
                            return circuit_breaker.call(
                                lambda: func(*args, **kwargs)
                            )
                        else:
                            return func(*args, **kwargs)
                    
                    except exceptions as e:
                        last_exception = e
                        attempt += 1
                        
                        if attempt < max_attempts:
                            delay = RetryHandler._calculate_delay(
                                attempt,
                                strategy,
                                base_delay,
                                max_delay,
                                backoff_multiplier,
                            )
                            logger.warning(
                                f"Attempt {attempt} failed for {func.__name__}: {e}. "
                                f"Retrying in {delay}s..."
                            )
                            time.sleep(delay)
                        else:
                            logger.error(
                                f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                            )
                
                raise RetryException(
                    f"Failed after {max_attempts} attempts: {last_exception}"
                )
            
            return wrapper
        return decorator
    
    @staticmethod
    def _calculate_delay(
        attempt: int,
        strategy: RetryStrategy,
        base_delay: float,
        max_delay: float,
        multiplier: float,
    ) -> float:
        """
        Calculate delay based on strategy.
        
        Args:
            attempt: Current attempt number
            strategy: Retry strategy
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            multiplier: Multiplier for backoff
            
        Returns:
            Calculated delay in seconds
        """
        if strategy == RetryStrategy.EXPONENTIAL:
            delay = base_delay * (multiplier ** (attempt - 1))
        elif strategy == RetryStrategy.LINEAR:
            delay = base_delay * attempt
        elif strategy == RetryStrategy.FIBONACCI:
            delay = base_delay * RetryHandler._fibonacci(attempt)
        else:  # FIXED
            delay = base_delay
        
        return min(delay, max_delay)
    
    @staticmethod
    def _fibonacci(n: int) -> int:
        """Calculate Fibonacci number."""
        if n <= 1:
            return 1
        a, b = 1, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b


def retry_on_exception(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
) -> Callable:
    """
    Simple retry decorator.
    
    Args:
        max_attempts: Maximum retry attempts
        delay: Initial delay in seconds
        backoff: Backoff multiplier
        
    Returns:
        Decorated function
    """
    return RetryHandler.retry(
        max_attempts=max_attempts,
        strategy=RetryStrategy.EXPONENTIAL,
        base_delay=delay,
        backoff_multiplier=backoff,
    )
