"""
Database manager for Partner App.
Handles database connections, queries, and data validation.
"""

from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from core.logger import logger
from config.settings import settings


class DatabaseManager:
    """Manage database connections and operations."""
    
    def __init__(self, db_url: str = None):
        """
        Initialize DatabaseManager.
        
        Args:
            db_url: Database connection URL
        """
        self.db_url = db_url or settings.get_database_url()
        self.engine = None
        self.session_factory = None
    
    def initialize(self) -> None:
        """Initialize database connection."""
        try:
            self.engine = create_engine(
                self.db_url,
                echo=settings.database.echo,
                pool_size=settings.database.pool_size,
                max_overflow=settings.database.max_overflow,
                pool_pre_ping=True,
            )
            self.session_factory = sessionmaker(bind=self.engine)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("Database connection initialized successfully")
        
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_session(self) -> Session:
        """
        Get database session.
        
        Returns:
            SQLAlchemy session
        """
        if not self.session_factory:
            self.initialize()
        
        return self.session_factory()
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute raw SQL query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result rows
        """
        session = self.get_session()
        try:
            result = session.execute(text(query), params or {})
            rows = [dict(row._mapping) for row in result]
            logger.debug(f"Query executed: {query[:100]}... - Rows: {len(rows)}")
            return rows
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
        finally:
            session.close()
    
    def execute_update(self, query: str, params: Dict[str, Any] = None) -> int:
        """
        Execute update/insert/delete query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        session = self.get_session()
        try:
            result = session.execute(text(query), params or {})
            session.commit()
            affected_rows = result.rowcount
            logger.info(f"Query executed: {query[:100]}... - Affected: {affected_rows}")
            return affected_rows
        except Exception as e:
            session.rollback()
            logger.error(f"Update query failed: {e}")
            raise
        finally:
            session.close()
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User record or None
        """
        try:
            query = "SELECT * FROM users WHERE email = :email"
            result = self.execute_query(query, {"email": email})
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Failed to get user by email: {e}")
            return None
    
    def create_user(
        self,
        email: str,
        password_hash: str,
        name: str = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Create new user.
        
        Args:
            email: User email
            password_hash: Hashed password
            name: User name
            
        Returns:
            Created user record
        """
        try:
            query = (
                "INSERT INTO users (email, password_hash, name, created_at) "
                "VALUES (:email, :password_hash, :name, NOW()) "
                "RETURNING *"
            )
            params = {
                "email": email,
                "password_hash": password_hash,
                "name": name,
            }
            result = self.execute_query(query, params)
            logger.info(f"User created: {email}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return None
    
    def update_user_status(self, user_id: int, status: str) -> bool:
        """
        Update user status.
        
        Args:
            user_id: User ID
            status: New status
            
        Returns:
            True if update successful
        """
        try:
            query = "UPDATE users SET status = :status WHERE id = :user_id"
            affected_rows = self.execute_update(
                query,
                {"status": status, "user_id": user_id}
            )
            return affected_rows > 0
        except Exception as e:
            logger.error(f"Failed to update user status: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            True if delete successful
        """
        try:
            query = "DELETE FROM users WHERE id = :user_id"
            affected_rows = self.execute_update(query, {"user_id": user_id})
            logger.info(f"User deleted: {user_id}")
            return affected_rows > 0
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            return False
    
    def close(self) -> None:
        """Close database connection."""
        try:
            if self.engine:
                self.engine.dispose()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Global database manager instance
db_manager = DatabaseManager()
