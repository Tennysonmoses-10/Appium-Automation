"""
REST API client for Partner App.
Handles all REST API interactions with authentication, retry logic, and validation.
"""

from typing import Optional, Dict, Any, Type
import httpx
from datetime import datetime
from core.logger import logger
from core.retry_handler import retry_on_exception
from config.settings import settings


class APIClient:
    """Base API client with common functionality."""
    
    def __init__(self, base_url: str = None, timeout: int = None):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API (defaults to settings)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or settings.api.base_url
        self.timeout = timeout or settings.api.timeout
        self.session = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            verify=settings.api.verify_ssl,
        )
        self.access_token: Optional[str] = None
    
    def set_auth_token(self, token: str) -> None:
        """
        Set authentication token.
        
        Args:
            token: Bearer token
        """
        self.access_token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.debug("Auth token set")
    
    def set_header(self, key: str, value: str) -> None:
        """
        Set custom header.
        
        Args:
            key: Header name
            value: Header value
        """
        self.session.headers[key] = value
    
    @retry_on_exception(max_attempts=3, delay=1.0)
    def get(
        self,
        endpoint: str,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ) -> httpx.Response:
        """
        Execute GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Custom headers
            
        Returns:
            Response object
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(
                endpoint,
                params=params,
                headers=headers,
            )
            logger.info(f"GET {url} - Status: {response.status_code}")
            response.raise_for_status()
            return response
        
        except httpx.HTTPStatusError as e:
            logger.error(f"GET request failed: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"GET request error: {e}")
            raise
    
    @retry_on_exception(max_attempts=3, delay=1.0)
    def post(
        self,
        endpoint: str,
        json: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ) -> httpx.Response:
        """
        Execute POST request.
        
        Args:
            endpoint: API endpoint
            json: JSON payload
            data: Form data
            headers: Custom headers
            
        Returns:
            Response object
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.post(
                endpoint,
                json=json,
                data=data,
                headers=headers,
            )
            logger.info(f"POST {url} - Status: {response.status_code}")
            response.raise_for_status()
            return response
        
        except httpx.HTTPStatusError as e:
            logger.error(f"POST request failed: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"POST request error: {e}")
            raise
    
    @retry_on_exception(max_attempts=3, delay=1.0)
    def put(
        self,
        endpoint: str,
        json: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ) -> httpx.Response:
        """
        Execute PUT request.
        
        Args:
            endpoint: API endpoint
            json: JSON payload
            headers: Custom headers
            
        Returns:
            Response object
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.put(
                endpoint,
                json=json,
                headers=headers,
            )
            logger.info(f"PUT {url} - Status: {response.status_code}")
            response.raise_for_status()
            return response
        
        except httpx.HTTPStatusError as e:
            logger.error(f"PUT request failed: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"PUT request error: {e}")
            raise
    
    @retry_on_exception(max_attempts=3, delay=1.0)
    def delete(
        self,
        endpoint: str,
        headers: Dict[str, str] = None,
    ) -> httpx.Response:
        """
        Execute DELETE request.
        
        Args:
            endpoint: API endpoint
            headers: Custom headers
            
        Returns:
            Response object
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.delete(
                endpoint,
                headers=headers,
            )
            logger.info(f"DELETE {url} - Status: {response.status_code}")
            response.raise_for_status()
            return response
        
        except httpx.HTTPStatusError as e:
            logger.error(f"DELETE request failed: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"DELETE request error: {e}")
            raise
    
    def close(self) -> None:
        """Close HTTP session."""
        try:
            self.session.close()
            logger.info("API client session closed")
        except Exception as e:
            logger.error(f"Error closing session: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class AuthAPIClient(APIClient):
    """API client for authentication endpoints."""
    
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login user.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Response with token and user info
        """
        try:
            payload = {
                "email": email,
                "password": password,
            }
            response = self.post("auth/login", json=payload)
            return response.json()
        except Exception as e:
            logger.error(f"Login API call failed: {e}")
            raise
    
    async def logout(self) -> None:
        """Logout user."""
        try:
            self.post("auth/logout")
            logger.info("User logged out via API")
        except Exception as e:
            logger.error(f"Logout API call failed: {e}")
            raise
    
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh authentication token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Response with new token
        """
        try:
            payload = {"refresh_token": refresh_token}
            response = self.post("auth/refresh", json=payload)
            return response.json()
        except Exception as e:
            logger.error(f"Refresh token API call failed: {e}")
            raise
    
    async def validate_token(self) -> bool:
        """
        Validate current token.
        
        Returns:
            True if token is valid
        """
        try:
            response = self.get("auth/validate")
            return response.status_code == 200
        except Exception:
            return False
