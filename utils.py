"""
Utility module for TauroBot 3.0
Centralizes common functionality to reduce code duplication
"""

import os
import logging
from typing import Optional, Callable, Any
import aiofiles


# Configure module logger
logger = logging.getLogger(__name__)


class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_error(error: Exception, message: str, logger_instance: logging.Logger = None) -> None:
        """
        Standard error handling with consistent logging
        
        Args:
            error: The exception that occurred
            message: Context message describing what failed
            logger_instance: Optional logger to use (defaults to module logger)
        """
        log = logger_instance or logger
        error_msg = f"{message}: {error}"
        log.error(error_msg)
    
    @staticmethod
    def safe_execute(func: Callable, default_return: Any = None, 
                     error_message: str = "Operation failed",
                     logger_instance: logging.Logger = None) -> Any:
        """
        Execute a function with error handling
        
        Args:
            func: Function to execute
            default_return: Value to return on error
            error_message: Context message for errors
            logger_instance: Optional logger to use
            
        Returns:
            Function result or default_return on error
        """
        try:
            return func()
        except Exception as e:
            ErrorHandler.handle_error(e, error_message, logger_instance)
            return default_return


class FileManager:
    """Centralized file operations"""
    
    @staticmethod
    def ensure_directory(file_path: str) -> bool:
        """
        Ensure directory exists for a file path
        
        Args:
            file_path: Path to file
            
        Returns:
            True if directory exists or was created successfully
        """
        try:
            directory = os.path.dirname(file_path)
            if directory:  # Only create if there's a directory component
                os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory for {file_path}: {e}")
            return False
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Check if file exists with error handling
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists
        """
        try:
            return os.path.exists(file_path)
        except Exception as e:
            logger.error(f"Error checking file existence {file_path}: {e}")
            return False
    
    @staticmethod
    def safe_remove(file_path: str) -> bool:
        """
        Safely remove a file with error handling
        
        Args:
            file_path: Path to file to remove
            
        Returns:
            True if file was removed or didn't exist
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception as e:
            logger.error(f"Failed to remove file {file_path}: {e}")
            return False
    
    @staticmethod
    async def async_read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """
        Async read file with error handling
        
        Args:
            file_path: Path to file
            encoding: File encoding
            
        Returns:
            File content or None on error
        """
        try:
            async with aiofiles.open(file_path, 'r', encoding=encoding) as f:
                return await f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return None
    
    @staticmethod
    async def async_write_file(file_path: str, content: str, 
                               encoding: str = 'utf-8') -> bool:
        """
        Async write file with error handling
        
        Args:
            file_path: Path to file
            content: Content to write
            encoding: File encoding
            
        Returns:
            True if successful
        """
        try:
            async with aiofiles.open(file_path, 'w', encoding=encoding) as f:
                await f.write(content)
            return True
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            return False


class ConfigLoader:
    """Centralized configuration loading"""
    
    @staticmethod
    def get_env_int(key: str, default: int) -> int:
        """
        Get integer from environment variable
        
        Args:
            key: Environment variable key
            default: Default value if not found or invalid
            
        Returns:
            Integer value
        """
        try:
            value = os.getenv(key)
            return int(value) if value else default
        except (ValueError, TypeError):
            logger.warning(f"Invalid integer value for {key}, using default: {default}")
            return default
    
    @staticmethod
    def get_env_float(key: str, default: float) -> float:
        """
        Get float from environment variable
        
        Args:
            key: Environment variable key
            default: Default value if not found or invalid
            
        Returns:
            Float value
        """
        try:
            value = os.getenv(key)
            return float(value) if value else default
        except (ValueError, TypeError):
            logger.warning(f"Invalid float value for {key}, using default: {default}")
            return default
    
    @staticmethod
    def get_env_list(key: str, separator: str = ',', 
                     item_type: type = str) -> list:
        """
        Get list from environment variable
        
        Args:
            key: Environment variable key
            separator: Character to split on
            item_type: Type to convert items to
            
        Returns:
            List of items
        """
        try:
            value = os.getenv(key, '')
            if not value:
                return []
            items = [x.strip() for x in value.split(separator) if x.strip()]
            if item_type == int:
                return [int(x) for x in items if x.isdigit()]
            return items
        except Exception as e:
            logger.warning(f"Error parsing list from {key}: {e}")
            return []


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger
    """
    return logging.getLogger(name)
